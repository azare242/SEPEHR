import datetime


def create_date(string: str):
    d1 = string.split(' ')
    d2 = d1[0].split('-')
    d3 = d1[1].split(':')
    di = {
        'year': int(d2[0]),
        'month': int(d2[1]),
        'day': int(d2[2]),
        'hour': int(d3[0]),
        'minute': int(d3[1]),
        'second': int(d3[2])
    }
    return datetime.datetime(di['year'], di['month'], di['day'], di['hour'], di['minute'], di['second'])