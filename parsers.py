from abc import ABC, abstractmethod
from colorama import init, Fore, Back, Style
from pprint import pprint
from string import Template

from requesters import AsyncGetRequester, AsyncPostRequester
from extracters import ZakupkiExtracter, ReestrNORPRIZExtracter
from data_models import Organization, SROMember
from bs4 import BeautifulSoup

import asyncio
import aiohttp


init()
headers = {
        'User-Agent'    : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.1.800 Yowser/2.5 Safari/537.36',
        'Content-Type' : 'application/json',
    }

class Parser(ABC):

    @abstractmethod
    def parse(self):
        pass

class AsyncParser(Parser):
    def __init__(self, requester, extracter, maker) -> None:
        super().__init__()
        self.__urls = None
        self.__bodies = None
        self.requester = requester
        self.extracter = extracter
        self.maker = maker 

    @property
    def urls(self):
        return self.__urls

    @urls.setter
    def urls(self, urls):
        self.__urls = urls
    
    @property
    def bodies(self):
        return self.__bodies

    @bodies.setter
    def bodies(self, bodies):
        self.__bodies = bodies

    async def _make_one_page_task(self, url, body, session):
        print(f'Create task: {url} {body}')
        data = await self.requester.make_request(url, body, session)
        print(f'Parsed: {url} {body}')
        return data
    
    @staticmethod
    def zip_urls_bodies(urls, bodies):
        url_len = len(urls)
        bodies_len = len(bodies)
        if all([url_len == 1, bodies_len != 1]):
            return zip(urls*bodies_len, bodies)
        elif all([url_len != 1, bodies_len == 1]):
            return zip(urls, bodies*url_len) 
        else:
            return zip(urls, bodies) 
        
    async def _get_many_page_tasks(self, urls, bodies):
        async with aiohttp.ClientSession(headers=headers) as session:
            tasks = [self._make_one_page_task(url, body, session)
                                    for url, body in self.zip_urls_bodies(urls=urls,
                                                                        bodies=bodies)]
            data = await asyncio.gather(*tasks)
        # await session.close()
        return data


    def parse(self):
        task = self._get_many_page_tasks(self.urls, 
                                         self.bodies)
        data = list(map(self.extracter.extract, asyncio.run(task)))
        # return self.maker.make(data)
        return list(map(list, data))


class ZakupkiParser(AsyncParser):

    def __init__(self, requester, extracter, maker) -> None:
        super().__init__(requester, extracter, maker)
        self.__urls = None
        self.__bodies = None
        recs_per_page = 500
        self.url_template = Template(f'https://zakupki.gov.ru/epz/dishonestsupplier/search/results.html?searchString=&morphology=on&search-filter=Дате+обновления&savedSearchSettingsIdHidden=&sortBy=UPDATE_DATE&pageNumber=$page&sortDirection=false&recordsPerPage=_{recs_per_page}&showLotsInfoHidden=false&fz223=on&ppRf615=on&dsStatuses=&inclusionDateFrom=&inclusionDateTo=&lastUpdateDateFrom=&lastUpdateDateTo=')
   

    @property
    def urls(self):
        if self.__urls is None:
            count = int(self.get_count_of_pages(self.url_template.substitute(page=1)))
            self.urls = [self.url_template.substitute(page=page_num) 
                                        for page_num in range(1, count+1)]
        return self.__urls
        
    @urls.setter
    def urls(self, urls):
        self.__urls = urls

    @property
    def bodies(self):
        if self.__bodies is None:
            self.bodies = [{}]
        return self.__bodies
    
    @bodies.setter
    def bodies(self, bodies):
        self.__bodies = bodies

    def get_count_of_pages(self, url):
        response = asyncio.run(self._get_many_page_tasks([url], [{}]))[0]
        return self.extracter.get_count_of_pages(response)


class ReestrNORPRIZParser(AsyncParser):

    def __init__(self, requester, extracter, maker) -> None:
        super().__init__(requester, extracter, maker)
        self.url = 'https://reestr.nopriz.ru/api/sro/all/member/list'
        self.__bodies = None
        self.__urls = [self.url]

    @staticmethod
    def get_body(num=1):
        return {
            "page": num,
            "pageCount": 10
        }

    @property
    def bodies(self):
        if self.__bodies is None:
            self.bodies = [{}]
        return self.__bodies
    
    @bodies.setter
    def bodies(self, bodies):
        self.__bodies = bodies

    @property
    def urls(self):
        if self.__urls is None:
            self.urls = [{}]
        return self.__urls
    
    @urls.setter
    def urls(self, urls):
        self.__urls = urls

    def get_count_of_pages(self):
        response = asyncio.run(self._get_many_page_tasks([self.url], 
                                                         [self.get_body()]))[0]
        pprint(len(response['json']['data']['data']))
        return self.extracter.get_count_of_pages(response)

    @property
    def bodies(self):
        if self.__bodies is None:
            self.count_of_pages = int(self.get_count_of_pages())
            print(f'Pages: {self.count_of_pages}')
            self.bodies = [self.get_body(num) 
                           for num in range(1, 10)]
        return self.__bodies
    
    @bodies.setter
    def bodies(self, bodies):
        self.__bodies = bodies



    # def parse(self):
    #     task = self._get_many_page_tasks()


    


if __name__ == '__main__':


    requester = AsyncPostRequester()
    extracter = ReestrNORPRIZExtracter()
    parser = ReestrNORPRIZParser(requester, 
                         extracter, 
                         None)
    data = parser.parse()
    

