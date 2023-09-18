import unittest
import requests
from pprint import pprint
from parsers import *
from bs4 import BeautifulSoup
from random import randbytes

record_template = """
<div class="search-registry-entry-block box-shadow-search-input">
    <div class="row no-gutters registry-entry__form mr-0">
        <div class="col-8 pr-0 mr-21px">
            <div class="registry-entry__header">
                <div class="row registry-entry__header-top">
                    <div class="col pr-0 d-flex align-items-center">
                        <div class="registry-entry__header-top__title text-truncate">
                            223-ФЗ
                        </div>
                        <div class="w-space-nowrap ml-auto registry-entry__header-top__icon">
                            <a href="https://zakupki.gov.ru/223/dishonest/public/supplier-print.html?supplierInfoId=16909" target="_blank">
                                <img src="/epz/static/img/icons/icon_print_small.svg" alt="Печатная форма">
                            </a>
                        </div>
                    </div>
                </div>
                <div class="d-flex registry-entry__header-mid align-items-center">
                    <div class="registry-entry__header-mid__number">
                        <a href="{URL}" target="_blank">
                            {ID}
                        </a>
                    </div>
                    <div class="registry-entry__header-mid__title">
                        Размещено
                    </div>
                </div>
            </div>
            <div class="registry-entry__body">
                <div class="registry-entry__body-block">
                    <div class="registry-entry__body-title">
                        Наименование (ФИО) недобросовестного поставщика
                    </div>
                    <div class="registry-entry__body-value">{NAME}</div>
                </div>
                <div class="registry-entry__body-block">
                    <div class="registry-entry__body-title">ИНН (аналог ИНН)</div>
                    <div class="registry-entry__body-value">{INN}</div>
                </div>
                <div class="registry-entry__body-block">
                    <div class="registry-entry__body-title">Страна</div>
                    <div class="registry-entry__body-value">Российская Федерация</div>
                </div>
            </div>
        </div>
        <div class="col d-flex flex-column registry-entry__right-block b-left">
            <div class="mt-auto">
                <div class="row">
                    <div class="col-6">
                        <div class="data-block__title">Включено</div>
                        <div class="data-block__value">{INCL_DATE}</div>
                    </div>
                    <div class="col-6">
                        <div class="data-block__title">Обновлено</div>
                        <div class="data-block__value">{UPD_DATE}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
"""
import random, string

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for _ in range(length))

class TestOrganizatonMaker(unittest.TestCase):
    def setUp(self):
        self.org_maker = OrganizatonMaker()
        self.answs = [randomword(5) for _ in range(5)]
        self.records = [
                            BeautifulSoup(record_template.format(
                                ID=f"{i}",
                                URL=f'{i}',
                                NAME=f"{i}",
                                INN=f"{i}",
                                INCL_DATE=f"{i}",
                                UPD_DATE=f"{i}"), 'lxml')
                            for i in self.answs
                        ]
        

    def test_get_id_and_url(self):
        for record, answ in zip(self.records, self.answs):
            self.assertEqual(self.org_maker._get_id_and_url(record), (answ, answ))

    def test_get_name(self):
        for record, answ in zip(self.records, self.answs):
            self.assertEqual(self.org_maker._get_name(record), answ)

    def test_get_inn(self):
        for record, answ in zip(self.records, self.answs):
            self.assertEqual(self.org_maker._get_inn(record), answ)

    def test_get_include_date(self):
        for record, answ in zip(self.records, self.answs):
            self.assertEqual(self.org_maker._get_include_date(record), answ)

    def test_get_update_date(self):
        for record, answ in zip(self.records, self.answs):
            self.assertEqual(self.org_maker._get_update_date(record), answ)



# req = requests.post(url=" http://rating.nopriz.ru/Home/GetFilteredList",
#                     files=(
#                         ("PageNumber", (None, 2)),
#                         ("ActivityDirectionId", (None, 1))
#                     ))
