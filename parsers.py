from abc import ABC, abstractmethod
from colorama import init, Fore, Back, Style

from requesters import AsyncGetRequester, AsyncPostRequester
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
    def __init__(self, requester, extracter, maker, urls, bodies) -> None:
        super().__init__()
        self._urls = urls
        self._bodies = bodies
        self.requester = requester
        self.extracter = extracter
        self.maker = maker 

    @property
    def urls(self):
        return self._urls

    @property.setter
    def urls(self, urls):
        self._urls = urls
    
    @property
    def bodies(self):
        return self._bodies

    @property.setter
    def bodies(self, bodies):
        self._bodies = bodies

    def _make_session(self, headers):
        self.session = aiohttp.ClientSession(headers=headers) 

    async def _close_session(self):
        await self.session.close()

    async def _make_one_page_task(self, url, body):
        return await self.requester.make_request(url, body)

    async def _get_many_page_tasks(self, urls, bodies):
        return asyncio.gather(*[self._make_one_page_task(url, body) 
                                for url, body in zip(urls, bodies)])
    
    async def parse(self):
        self._make_session()
        task = self._get_many_page_tasks(self.urls, 
                                         self.bodies)
        data = self.extracter(asyncio.run(task))
        self._close_session()
        return self.maker.make(data)


class ZakupkiParser(AsyncParser):
    
    def __init__(self, requester, extracter, maker, url, bodies) -> None:
        super().__init__(requester, extracter, maker, url, bodies)
        self._recs_per_pages = 500
    
    @property
    def recs_per_pages(self):
        return self._recs_per_pages
    
    @property.setter
    def recs_per_pages(self, value):
        if value <= 0:
            raise ValueError('The number of entries on the page must be greater than zero')
        self._recs_per_pages = value
    def parse(self):
        

    




