from abc import ABC, abstractmethod
from string import Template
from dataclasses import dataclass, asdict, astuple
from datetime import datetime
from pprint import pprint
from functools import reduce
from json import dump
from typing import Any, Union
from time import sleep
from random import randint
import csv
import timeit

from requests import get, post
from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style

import asyncio
import aiohttp


init()
headers = {
        'User-Agent'    : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.1.800 Yowser/2.5 Safari/537.36',
        'Content-Type' : 'application/json',
    }
class Saver:
    @staticmethod
    def save(data, path):
        pass

class JSONSaver(Saver):
    
    @staticmethod
    def save(data, path) -> None:
        with open(path, 'w', encoding='utf-8') as file:
            dump(data, file, indent=4, ensure_ascii=False)

class CSVSaver(Saver):
    
    @staticmethod
    def save(data, path) -> None:
        with open(path, 'w', newline='\n') as file:
            csv.writer(file).writerows(data)

@dataclass
class Organization:

    id           : str
    name         : str
    inn          : str
    url          : str
    date_include : datetime
    date_updated : datetime

@dataclass
class Organization:

    id           : str
    full_description         : str
    short_description          : str
    city : str
    address : str
    
class Maker(ABC):
    
    @abstractmethod
    def make(data):
        pass

def make_random_sleep(from_, to):
    sleep(randint(from_, to)/10)

class OrganizatonMaker:
    
    @staticmethod
    def _get_id_and_url(record) -> tuple:
        try:
            tag = record.find('div', class_='registry-entry__header-mid__number').find('a')
        except Exception as e:
            print(e)
            url, id = None, None
        else:
            url = tag.get('href').strip()
            id = tag.text.strip().split()[-1]
        return id, url
    
    @staticmethod
    def _get_name(record) -> str:
        try:
            return record.find('div', class_='registry-entry__body-value').text.strip()
        except Exception:
            return None
        
    @staticmethod
    def _get_inn(record) -> str:
        try:
            return record.find_all('div', class_='registry-entry__body-value')[1].text.strip()
        except Exception:
            return None

    @staticmethod
    def _get_date(record, num=0) -> str:
        try:
            return record.find('div', class_='mt-auto')\
                         .find_all('div', class_='data-block__value')[num].text.strip()
        except Exception:
            return None

    @classmethod
    def _get_include_date(cls, record) -> str:
        return cls._get_date(record)
    
    @classmethod
    def _get_update_date(cls, record) -> str:
        return cls._get_date(record, 1)

    @classmethod
    def make(cls, record) -> Organization:
        name = cls._get_name(record)
        id, url = cls._get_id_and_url(record)
        inn = cls._get_inn(record)
        date_include = cls._get_include_date(record)
        date_update = cls._get_update_date(record)
        return Organization(id, name, inn, url, date_include, date_update)
            

class Converter(ABC):

    @abstractmethod
    def _convert_one(data: Any):
        pass            

    @abstractmethod
    def _convert_many(data: Any):
        pass

    @abstractmethod
    def convert(cls, data: Any, *args, **kwargs):
        return cls._convert_one(data) if isinstance(data, Organization)\
            else cls._convert_many(data)

class ConverterOrganizationToJSON(Converter):
    
    @staticmethod
    def _convert_one(organization: Organization) -> dict:
        return asdict(organization)
    
    @classmethod
    def _convert_many(cls, organizations: [Organization]) -> [dict]:
        return [cls._convert_one(org) for org in organizations]


class ConverterOrganizatonToCVS(Converter):
    
    @staticmethod
    def _convert_one(organization: Organization, sep : str = ',') -> str:
        return sep.join(astuple(organization))     

    @classmethod
    def _convert_many(cls, organizations: [Organization], sep : str = ',') -> str:
        return '\n'.join(cls._convert_one(organization, sep) 
                          for organization in organizations)
    @classmethod
    def convert(cls, data: Any, sep : str = ',', *args, **kwargs):
        return cls._convert_one(data, sep) if isinstance(data, Organization)\
            else cls._convert_many(data, sep)

class Parser(ABC):

    @abstractmethod
    def parse(self):
        pass

class ZakupkiParser(Parser):
    recs_per_page = 500
    url = Template(f'https://zakupki.gov.ru/epz/dishonestsupplier/search/results.html?searchString=&morphology=on&search-filter=Дате+обновления&savedSearchSettingsIdHidden=&sortBy=UPDATE_DATE&pageNumber=$page&sortDirection=false&recordsPerPage=_{recs_per_page}&showLotsInfoHidden=false&fz223=on&ppRf615=on&dsStatuses=&inclusionDateFrom=&inclusionDateTo=&lastUpdateDateFrom=&lastUpdateDateTo=')
    
    @classmethod
    def get_url_by_page_num(cls, page_num) -> str:
        return cls.url.substitute(page=page_num)

    @classmethod
    def get_page_by_page_num(cls, num=1) -> str:
        url = cls.get_url_by_page_num(num)
        return get(url).text

    @classmethod
    async def async_get_page_by_page_num(cls, num=1) -> asyncio.coroutine:
        url = cls.get_url_by_page_num(num)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                page = await response.text()
                print(f"Parsed: {num}")

        return page

    @classmethod
    async def get_pages(cls, page_count) -> asyncio.coroutine:
        pages = asyncio.gather(*(cls.async_get_page_by_page_num(page_num) 
                    for page_num in range(1, page_count+1)))
        return await pages
    
    @staticmethod
    def get_soup_from_html_page(html_page) -> BeautifulSoup:
        # print(html_page)
        return BeautifulSoup(html_page, 'lxml')

    @classmethod
    def _get_count_pages(cls) -> int:
        page = cls.get_soup_from_html_page(cls.get_page_by_page_num())
        return int(page.find_all('li', class_='page')[-1].text.strip())
    
    @classmethod
    def get_records_from_page(cls, page) -> [str]:
        return cls.get_soup_from_html_page(page).find('div', class_='search-registry-entrys-block')\
                                             .find_all('div', class_='search-registry-entry-block')
        
    @classmethod
    def pasre_page(cls, page, org_maker) -> [Organization]:
        records = cls.get_records_from_page(page)
        return [
            org_maker.make(record) for record in records
        ]

    @classmethod
    def parse(cls, org_maker) -> [Organization]:
        page_count = cls._get_count_pages()

        pages = cls.get_pages(page_count)
        pages = asyncio.run(pages)

        print('SCRAPING')
        return reduce(
            lambda a, b: a + b, [cls.pasre_page(page, org_maker) for page in pages]
        )

class NORPRIZParser(Parser):
    url = 'https://reestr.nopriz.ru/api/sro/all/member/list'

    @staticmethod
    def get_body(num=1):
        return {
            "page": num,
            "pageCount": 5000
        }
        

    @classmethod
    def get_page_by_page_num(cls, num=1) -> Any:
        r = post(cls.url, 
                    headers=headers, 
                    json=cls.get_body(num))
        try:    
            return r.json()
        except Exception as e:
            print(f'Status code: {r.status_code}, {e}')

    @classmethod
    def _get_count_pages(cls) -> int:
        return int(cls.get_page_by_page_num().get('data').get('countPages', 1))

    @classmethod
    async def get_one_page(cls, session, request_body):
        page_num = request_body["page"]
        print(f'Created task: {page_num}')
        async with session.post(cls.url, data=request_body) as response:
            page = await response.json()
            print(f' - parced: {page_num}')
            return page

    @classmethod
    async def get_many_pages(cls, request_bodies):
        session = aiohttp.ClientSession(headers=headers)
        tasks = [cls.get_one_page(session, request_body)
                        for request_body in request_bodies]
        data = await asyncio.gather(*tasks)
        await session.close()
        return data

    @staticmethod
    def _extract_one(data: dict) -> [dict]:
        return data.get('data').get('data')
  
    @classmethod
    def _extract_many(cls, data: [Any]) -> [dict]:
        return reduce(
            lambda a, b: a + b, 
            [cls._extract_one(page) for page in data]
        )
    
    @classmethod
    def extract_data(cls, data):
        return cls._extract_one(data) if isinstance(data, dict)\
            else cls._extract_many(data)

    
    

    @classmethod
    def parse(cls):
        page_num = cls._get_count_pages()
        print(f'Total pages: {page_num}')
        request_bodies = map(cls.get_body, range(1, page_num+1))
        future = cls.get_many_pages(request_bodies)
        data = asyncio.run(future)
        pprint(cls.extract_data(data))
        return data


if __name__ == '__main__':
    parser = NORPRIZParser()
    parser.parse()




