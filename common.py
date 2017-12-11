import re


def price_filter(original_function):
    def wrapper(*args, **kwargs):
        prcstr = original_function(*args, **kwargs)
        if not prcstr:
            return None
        prcstr = prcstr.replace(",", "")
        reg = re.search(r"\d+", prcstr)
        return reg.group() if reg else None
    return wrapper
