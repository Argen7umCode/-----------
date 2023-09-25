from abc import ABC, abstractmethod
import aiohttp

from aiohttp import ClientResponse
from bs4 import BeautifulSoup

class Extracter(ABC):

    @abstractmethod
    def extract(self, responce: ClientResponse):
        pass

class ZakupkiExtracter(Extracter):
    
    @staticmethod
    def get_soup_from_page(page):
        return BeautifulSoup(page, 'lxml')

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
            return record.find_all('div', class_='registry-entry__body-value')[1].text\
                                                                                 .strip()
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

    @staticmethod
    def get_page_from_responce(response):
        return response.text()

    def extract(responce: ClientResponse):

        
        name = cls._get_name(record)
        id, url = cls._get_id_and_url(record)
        inn = cls._get_inn(record)
        date_include = cls._get_include_date(record)
        date_update = cls._get_update_date(record)
