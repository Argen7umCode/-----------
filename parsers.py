from abc import ABC, abstractmethod
from string import Template

from requests import get, post
from bs4 import BeautifulSoup

import asyncio


def get_user_agent():
    return 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.1.800 Yowser/2.5 Safari/537.36'



class Parser:

    @abstractmethod
    def parse(self):
        ...

class ZakupkiParser(Parser):

    url = Template(r'https://zakupki.gov.ru/epz/dishonestsupplier/search/results.html?searchString=&morphology=on&search-filter=Дате+обновления&savedSearchSettingsIdHidden=&sortBy=UPDATE_DATE&pageNumber=$page&sortDirection=false&recordsPerPage=_500&showLotsInfoHidden=false&fz223=on&ppRf615=on&dsStatuses=&inclusionDateFrom=&inclusionDateTo=&lastUpdateDateFrom=&lastUpdateDateTo=')

    @classmethod
    def __get_count_pages(cls):
        url = cls.url.substitute(page=1)
        r = BeautifulSoup(get(url, headers={'user-agent' : get_user_agent()}).text, "html.parser")
        return int(r.find_all('li', class_='page')[-1].text.strip())


    @classmethod
    def pasre_page()

    @classmethod
    async def parse(cls):
        pass
        


if __name__ == "__main__":
    print(ZakupkiParser().get_count_pages())

# async def foo():
#     print('Running in foo')
#     await asyncio.sleep(10)
#     print('Explicit context switch to foo again')


# async def bar():
#     print('Explicit context to bar')
#     await asyncio.sleep(10)
#     print('Implicit context switch back to bar')


# ioloop = asyncio.get_event_loop()
# tasks = [ioloop.create_task(foo()), ioloop.create_task(bar())]
# wait_tasks = asyncio.wait(tasks)
# ioloop.run_until_complete(wait_tasks)
# ioloop.close()