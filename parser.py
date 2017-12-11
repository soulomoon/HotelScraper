import pandas as pd
import re
from bs4 import BeautifulSoup
from names import *
from data import retrieve_files_path, save_file
from common import price_filter, strip


def parse_text(item, text):
    ele = item.find(class_=text)
    if ele and ele.string:
        return str(ele.string).strip()


def parse_items(text, class_name):
    """parse_items

    :param text: html text to parse
    :param class_name: class_name to find that you can get single room info
    """
    soup = BeautifulSoup(text, "html.parser")
    return soup.find_all(class_=class_name)


def airbnb_parse_items(text):
    return parse_items(text, AIRBNB_ITEM)


def airbnb_parse_name(item):
    return parse_text(item, AIRBNB_NAME)


def airbnb_parse_type(item):
    item = item.find(class_=AIRBNB_TYPE)
    if item:
        return [i for i in item.strings][0]


def airbnb_parse_beds(item):
    item = item.find(class_=AIRBNB_TYPE)
    if item:
        return [i for i in item.strings][-1]


def airbnb_parse_rating(item):
    item = item.find(class_=AIRBNB_RATING)
    if item:
        span = item.find("span")
        if hasattr(span, "aria-label"):
            return span["aria-label"]


@price_filter
def airbnb_parse_price(item):
    item = item.find(class_=AIRBNB_PRICE)
    if item:
        spans = item.find_all("span")
        if len(spans) > 2:
            price = spans[2].string
            return price


def booking_parse_items(text):
    return parse_items(text, BOOKING_ITEM)


def booking_parse_name(item):
    return parse_text(item, BOOKING_NAME)


def booking_parse_district(item):
    whole = parse_text(item, BOOKING_DISTRICT)
    return whole.split(',')[0] if whole else None


def booking_parse_rating(item):
    return parse_text(item, BOOKING_RATING)


@price_filter
def booking_parse_price(item):
    ele = item.find(class_=BOOKING_PRICE)
    if ele and ele.b and ele.b.string:
        return str(ele.b.string).strip()


BOOKING_DICT = {
    "NAME": booking_parse_name,
    "DISTRICT": booking_parse_district,
    "RATING": booking_parse_rating,
    "PRICE": booking_parse_price,
    "parser": booking_parse_items
}

AIRBNB_DICT = {
    "NAME": airbnb_parse_name,
    "TYPE": airbnb_parse_type,
    "BEDS": airbnb_parse_beds,
    "RATING": airbnb_parse_rating,
    "PRICE": airbnb_parse_price,
    "parser": airbnb_parse_items
}


def form_items_from_path(path, type_dict):
    """form_items_from_path
    split file in path with configuration dict
    :param path:
    :param type_dict:
    """
    if "parser" not in type_dict:
        raise "please impelement parser"
    with open(path, 'r', encoding='utf-8') as f:
        return type_dict["parser"](f)


def form_df_from_items(items, type_dict):
    container = {}
    for name, func in type_dict.items():
        if name != "parser":
            values = [strip(func(item)) for item in items]
            container[name] = values
    df = pd.DataFrame.from_dict(container)
    return df


def form_df_from_path(path, type_dict):
    items = form_items_from_path(path, type_dict)
    return form_df_from_items(items, type_dict)


def form_booking_df_from_path(path):
    return form_df_from_path(path, BOOKING_DICT)


def form_airbnb_df_from_path(path):
    return form_df_from_path(path, AIRBNB_DICT)


def combine_df(form_func, pattern):
    paths = retrieve_files_path(pattern)
    dataframes = [form_func(path) for path in paths]
    df = pd.DataFrame()
    for frame in dataframes:
        df = df.append(frame, ignore_index=True)
    return df


def get_df(form_func, scraper_name, store_path):
    df = combine_df(form_func, scraper_name)
    df.to_csv(store_path, index=False, encoding='utf-8')
    print(df)


def get_booking_df():
    return get_df(
        form_booking_df_from_path,
        "BookingScraper",
        "data/Bookingdataframes.csv")


def get_airbnb_df():
    return get_df(
        form_airbnb_df_from_path,
        "AirbnbScraper",
        "data/airbnbdataframes.csv")


def get_special_df():
    return get_df(
        form_booking_df_from_path,
        "SpecialBookingScraper",
        "data/specialdataframes.csv")


def run():
    get_booking_df()
    get_special_df()
    get_airbnb_df()


if __name__ == "__main__":
    run()
