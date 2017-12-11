import re
from abc import ABC, abstractproperty
from selenium import webdriver
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urlparse, urlencode
from names import BOOKING_SPECIAL_DICT, BOOKING_QUERY_DICT, AIRBNB_QUERY_DICT
from data import *


class PagingScraper(ABC):
    def __init__(self, *args, **kwargs):
        self._url = self.url_search + urlencode(self.init_query_dict)
        self.source_list = []
        self.counter = 0

    def __enter__(self):
        self.browser = webdriver.Firefox()
        print("loading begin")
        self.collect()
        return self

    def __exit__(self, type, value, traceback):
        self.browser.close()

    def collect(self):
        print("loading: {}".format(self._url))
        self.browser.get(self._url)
        # self.source_list.append(self.browser.page_source)
        if self.counter == 0:
            delete_file(self.__class__.__name__)
        save_file(self.__class__.__name__ +
                  str(self.counter), self.browser.page_source)
        print("fetching data done")
        self.counter += 1

    def update_url(self, prprty, value):
        """update_url

        :param prprty:
        :param value:
        """
        # update query
        parsed = urlparse(self._url)
        query_dict = parse_qs(parsed.query)
        query_dict.update([(prprty, [value])])
        query = urlencode(query_dict, doseq=True)
        # parse url and replace querystring
        parsed = parsed._replace(query=query)
        print(parsed.geturl())
        self._url = parsed.geturl()

    def set_next_url(self):
        print("finding next url")
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        url_rest = self.fetch_next_url(soup)
        if url_rest and url_rest.has_attr('href'):
            self._url = self.url_home + url_rest['href']
            print("next url found:{}".format(self._url))
            return self._url
        print("next url not found for: {}".format(self._url))

    def get_all_pages(self):
        while self.set_next_url():
            self.collect()
        return self.source_list

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
    def init_query_dict(self):
        pass


class BookingScraper(PagingScraper):
    def __init__(self, place, bdate, edate):
        """__init__
        :param place:
        :param bdate: 20xx-xx-xx
        :param edate: 20xx-xx-xx
        """
        super().__init__()
        self.update_url("ss", place)
        self.update_url("checkin_year_month_monthday", bdate)
        self.update_url("checkout_year_month_monthday", edate)

    def collect(self):
        print("loading: {}".format(self._url))
        self.browser.get(self._url)
        self.detour(self.browser.page_source)
        if self.counter == 0:
            delete_file(self.__class__.__name__)
        save_file(self.__class__.__name__ +
                  str(self.counter), self.browser.page_source)
        print("fetching data done")
        self.counter += 1

    def detour(self, html):
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        url_rest = soup.find("a", class_="item_name_link")
        if url_rest and url_rest.has_attr('href'):
            print("multiple rezult taking a detour")
            self._url = self.url_home + url_rest['href']
            self.browser.get(self._url)


    @property
    def init_query_dict(self):
        return BOOKING_QUERY_DICT.copy()

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
    def init_query_dict(self):
        return BOOKING_SPECIAL_DICT.copy()


class AirbnbScraper(PagingScraper):
    def __init__(self, place, bdate, edate):
        """__init__
        :param place:
        :param bdate: 20xx-xx-xx
        :param edate: 20xx-xx-xx
        """
        self.place = place
        super().__init__()
        print(self._url)
        self.update_url("checkin", bdate)
        self.update_url("checkout", edate)
        print(self._url)

    @property
    def init_query_dict(self):
        return AIRBNB_QUERY_DICT.copy()

    @property
    def url_home(self):
        return "https://www.airbnb.com"

    @property
    def url_search(self):
        return "{home}/s/{place}/homes?".format(
            home=self.url_home, place=self.place)

    def fetch_next_url(self, soup):
        li = soup.find("li", class_="_b8vexar")
        if li:
            return li.find("a", class_="_1ko8une")


def get_all_pages(scraper, place, indate, outdate):
    with scraper(place, indate, outdate) as br:
        return br.get_all_pages()
    raise "scraper({}): scraping make a mistake, please restart".format(
        type(scraper).__name__)


def run(place, indate, outdate):
    all_pages = get_all_pages(BookingScraper, place, indate, outdate)
    airbnb_all_pages = get_all_pages(AirbnbScraper, place, indate, outdate)
    all_special_pages = get_all_pages(
        SpecialBookingScraper, place, indate, outdate)


if __name__ == "__main__":
    run('guangzhou', '2017-12-19', '2017-12-20')
