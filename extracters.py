from abc import ABC, abstractmethod
from functools import reduce
from typing import Any
from bs4 import BeautifulSoup

class Extracter(ABC):

    @staticmethod
    def get_html_page_from_response(response):
        return(response.get('html'))

    @staticmethod
    def get_json_from_response(response):
        return(response.get('json'))

    @staticmethod
    def get_status_code_page_from_response(response):
        return(response.get('status'))

    @abstractmethod
    def extract(self, responce: dict):
        pass

class ZakupkiExtracter(Extracter):
    
    @staticmethod
    def get_soup_from_html_page(page):
        return BeautifulSoup(page, 'lxml')

    def get_count_of_pages(self, response):
        page = self.get_soup_from_html_page(
                self.get_html_page_from_response(response))
        return int(page.find_all('li', class_='page')[-1].text.strip())
    

    def get_records_from_page(self, page) -> [str]:

        return self.get_soup_from_html_page(page).find('div', class_='search-registry-entrys-block')\
                                             .find_all('div', class_='search-registry-entry-block')
    

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


    def extract(self, responce: dict):
        page = self.get_html_page_from_response(responce)
        records = self.get_records_from_page(page)
        
        for record in records:
            id, url = self._get_id_and_url(record)
            yield {
                'name' : self._get_name(record),
                'id'   : id,
                'url'  : url,
                'date_include' : self._get_include_date(record),
                'date_update' : self._get_update_date(record)
            }


class ReestrNORPRIZExtracter(Extracter):

    def get_count_of_pages(self, response):
        json_data = self.get_json_from_response(response)
        return json_data.get('data').get('countPages', 1)
    
    
    def _extract_one(self, response: dict) -> [dict]:
        data = self.get_json_from_response(response)
        return data.get('data').get('data')
  

    def _extract_many(self, responses: [Any]) -> [dict]:
        return reduce(
            lambda a, b: a + b, 
            [self._extract_one(response) for response in responses]
        )

    def extract(self, response):
        return self._extract_one(response) if isinstance(response, dict)\
            else self._extract_many(response)
