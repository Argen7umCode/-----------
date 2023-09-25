from abc import ABC, abstractmethod
from colorama import init, Fore, Back, Style
from pprint import pprint


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
        self.__urls = urls
        self.__bodies = bodies
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
        return await self.requester.make_request(url, body, session)

    async def _get_many_page_tasks(self, urls, bodies):
        session = aiohttp.ClientSession(headers=headers) 
        tasks = [self._make_one_page_task(url, body, session)
                                for url, body in zip(urls, bodies)]
        data = await asyncio.gather(*tasks)
        await session.close()
        return data


    def parse(self):
        task = self._get_many_page_tasks(self.urls, 
                                         self.bodies)
        # data = self.extracter()
        data = asyncio.run(task)
        # return self.maker.make(data)

        return data



if __name__ == '__main__':
    requester = AsyncGetRequester()
    parser = AsyncParser(requester, None, None, ['https://stackoverflow.com/questions/64007067/async-processing-of-function-requests-using-asyncio'] * 3, [{}]*3)
    pprint(parser.parse())
    

