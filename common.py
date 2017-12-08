from urllib.parse import parse_qs

def url_to_json(url):
    params_dict = parse_qs(url)


