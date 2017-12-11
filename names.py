from types import MappingProxyType

BOOKING_ITEM = "sr_item"
BOOKING_NAME = "sr-hotel__name"
BOOKING_DISTRICT = "district_link"
BOOKING_RATING = "review-score-badge"
BOOKING_PRICE = "availprice"

AIRBNB_ITEM = "_1mpo9ida"
AIRBNB_NAME = "_o0r6eqm"
AIRBNB_TYPE= "_1127fdt6"
AIRBNB_BEDS= "_1127fdt6"
AIRBNB_RATING = "_1uyixqdu"
AIRBNB_PRICE = "_hylizj6"

BOOKING_QUERY_DICT = MappingProxyType({
    "checkin_year_month_monthday": "2017-12-14",
    "checkout_year_month_monthday": "2017-12-15",
    "ss": "guangzhou",
    "nflt": "class=4;class=3;class=5;",
    "rows": "40",
    "offset": "0",
    "selected_currency": "HKD"
})
BOOKING_SPECIAL_DICT = dict(BOOKING_QUERY_DICT)
BOOKING_SPECIAL_DICT.update({"nflt": "class=4;class=3;class=5;fc=2;mealplan=1;hotelfacility=16;hotelfacility=107;hotelfacility=28;popular_activities=11;"})
BOOKING_SPECIAL_DICT = MappingProxyType(BOOKING_SPECIAL_DICT)

AIRBNB_QUERY_DICT = MappingProxyType({
    "checkin": "2017-12-09",
    "checkout": "2017-12-15"
})

FOLDER = "data"
