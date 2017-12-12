'''
(c) 2017 Oleksandr Bogomaz

Date utils.
'''


import datetime


def week(year, month, day):
    d = datetime.date(year, month, day)
    e = datetime.date(1980, 1, 13)
    diff = d-e
    return diff.days//7+1
