def validate_date(self, date):
    dl = date.split('-')
    if len(dl) != 3:
        raise 'date imput error, should be in formate xxxx-xx-xx'
    return dl

