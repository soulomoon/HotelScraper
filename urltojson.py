from urllib.parse import parse_qs

def url_to_dict(url):
    params_dict = parse_qs(url)
    return params_dict

if __name__ == "__main__":
    url = r"https://www.booking.com/searchresults.html?aid=304142&label=gen173nr-1FCAQoggJCEHNlYXJjaF9ndWFuZ3pob3VIM1gEaDGIAQGYATG4AQfIAQ_YAQHoAQH4AQOSAgF5qAID&sid=c4670d5f0cfcccba966645bc04820083&checkin_year_month_monthday=2017-12-14&checkout_year_month_monthday=2017-12-15&class_interval=1&dest_id=-1907161&dest_type=city&label_click=undef&raw_dest_type=city&room1=A%2CA&rows=40&sb_price_type=total&ss=guangzhou&ssb=empty&nflt=class%3D4%3Bclass%3D3%3Bclass%3D5%3Bfc%3D2%3Bmealplan%3D1%3Bhotelfacility%3D16%3Bpopular_activities%3D11%3B&lsf=popular_activities%7C11%7C62&unchecked_filter=popular_activities"
    url_to_json(url)
