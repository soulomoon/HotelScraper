import re
from abc import ABC, abstractproperty
from selenium import webdriver
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from parser import *
from cssname import SPECIAL_URL
from urltojson import url_to_dict

PARAMS_DICT = {
    "checkin_year_month_monthday": "2017-12-14",
    "checkout_year_month_monthday": "2017-12-15",
    "ss": "guangzhou",
    "nflt": "class=4;class=3;class=5;",
    "rows": "40",
    "offset": "0",
    "selected_currency": "HKD"
}

SPECIAL_DICT = PARAMS_DICT.copy()
SPECIAL_DICT.update({"nflt": "class=4;class=3;class=5;fc=2;mealplan=1;hotelfacility=16;hotelfacility=107;hotelfacility=28;popular_activities=11;"})

class PagingScraper(ABC):
    def __init__(self, *args, **kwargs):
        self.source_list = []
        self._url = self.url_search + urlencode(self.params_dict)

    def __enter__(self):
        self.browser = webdriver.Firefox()
        self.collect()
        input()
        return self

    def __exit__(self, type, value, traceback):
        self.browser.close()

    def collect(self):
        self.browser.get(self._url)
        self.source_list.append(self.browser.page_source)

    def update(self, prprty, value):
        self.params_dict.update([(prprty, value)])

    def set_next_url(self):
        return None
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        url_rest = self.fetch_next_url(soup)
        if url_rest and url_rest.has_attr('href'):
            self._url = self.url_home + url_rest['href']
            return self._url

    @abstractproperty
    def fetch_next_url(self, soup):
        pass

    @abstractproperty
    def url_home(self):
        pass

    @abstractproperty
    def url_search(self):
        pass

    @abstractproperty
    def params_dict(self):
        pass

    @abstractproperty
    def get_init_dict(self):
        pass

    @property
    def params_dict(self):
        if not hasattr(self, "_params_dict"):
            self._params_dict =  self.get_init_dict
        return self._params_dict

    @params_dict.setter
    def params_dict(self, value):
        self._params_dict = value

    def get_all_pages(self):
        while self.set_next_url():
            self.collect()
        return self.source_list



class BookingScraper(PagingScraper):
    def __init__(self, place, bdate, edate):
        """__init__
        :param place:
        :param bdate: 20xx-xx-xx
        :param edate: 20xx-xx-xx
        """
        super().__init__()
        self.update("ss", place)
        self.update("checkin_year_month_monthday", bdate)
        self.update("checkout_year_month_monthday", edate)

    @property
    def get_init_dict(self):
        return PARAMS_DICT.copy()

    @property
    def url_home(self):
        return "https://www.booking.com"

    @property
    def url_search(self):
        return "{}/searchresults.html?".format(self.url_home)

    def fetch_next_url(self, soup):
        return soup.find("a", class_="paging-next")


class SpecialBookingScraper(BookingScraper):
    @property
    def get_init_dict(self):
        return SPECIAL_DICT.copy()

def get_all_pages(scraper, place, indate, outdate):
    with scraper(place, indate, outdate) as br:
        return br.get_all_pages()
    raise "scraper({}): scraping make a mistake, please restart".format(type(scraper).__name__)

def run(place, indate, outdate):
    all_pages = get_all_pages(SpecialBookingScraper, place, indate, outdate)
    all_special_pages = get_all_pages(SpecialBookingScraper, place, indate, outdate)



if __name__ == "__main__":
    run('guangzhou', '2018-05-03', '2018-05-04')

    textfile = open('textfile.txt', 'w', encoding='utf-8')
    textfile.write(all_pages[0])
    textfile.close()
