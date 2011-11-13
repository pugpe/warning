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

    trs = soup.findAll('tr', attrs={'bgcolor': re.compile('#EDF3F9|#FFFFFF')})

    indexes = {}
    for tr in trs:
        city = get_city(tr)
        indexes[slugify(city)] = (city, get_index(tr))

    return indexes

def english_mep():
    '''
    List of indexes of english_mep
    http://english.mep.gov.cn/datarb/htm/index_1.html
    '''

    url = 'http://english.mep.gov.cn/datarb/htm/index_1.html'
    soup = BeautifulSoup(requests.get(url).content)

    trs = soup.findAll('tr', {'class': '.menu12'})

    indexes = {}
    for tr in trs:
        city_name = tr.td.next
        index = city_name.next.next
        indexes[slugify(city_name)] = (city_name, index)

    return indexes

if __name__ == '__main__':
    d_indexes = air_now()
