# -*- coding:utf-8 -*-
import re
import requests

from BeautifulSoup import BeautifulSoup


def slugify(s):
    return s.lower().replace(' ', '-')


def air_now():
    '''
    List of indexes of airnow:
    http://www.airnow.gov/index.cfm?action=airnow.national_summary
    '''
    url = 'http://www.airnow.gov/index.cfm?action=airnow.national_summary'
    soup = BeautifulSoup(requests.get(url).content)

    get_city = lambda tr: tr.find('a').getText()
    get_index = lambda tr: tr.findChildren('td')[-3].getText()

    trs = soup.findAll('tr', attrs={'bgcolor':re.compile('#EDF3F9|#FFFFFF')})

    indexes = {}
    for tr in trs:
        city = get_city(tr)
        indexes[slugify(city)] = (city, get_index(tr))

    return indexes


if __name__ == '__main__':
    d_indexes = air_now()
