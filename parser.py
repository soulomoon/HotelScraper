from bs4 import BeautifulSoup
from cssname import *


def parse_items(text):
    soup = BeautifulSoup(text, "html.parser")
    all_iterms = soup.find_all(class_=ITERM)
    return all_iterms

def parse_text(item, text):
    ele = item.find(class_=text)
    if ele and ele.string:
        return str(ele.string).strip()

def parse_hotel_name(item):
    return parse_text(item, HOTEL_NAME)

def parse_district(item):
    whole = parse_text(item, DISTRICT)
    return whole.split(',')[0] if whole else None

def parse_rating(item):
    return parse_text(item, RATING)

def parse_price(item):
    ele = item.find(class_=PRICE)
    print(ele)
    if ele and ele.b:
        if ele.b.string:
            return str(ele.b.string).strip()


if __name__ == "__main__":
    with open('textfile.txt', 'r', encoding='utf-8') as f:
        items = parse_items(f)
        names = [parse_hotel_name(item) for item in items]
        dises = [parse_district(item) for item in items]
        ratings = [parse_rating(item) for item in items]
        prices = [parse_price(item) for item in items]
        for i in range(len(items)):
#            print(items[i])
            print(names[i])
            print(dises[i])
            print(ratings[i])
            print(prices[i])

        print(len(items))
        print(len(names))
        print(len(dises))
        print(len(ratings))

