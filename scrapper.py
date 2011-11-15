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
    List of indexes of english_mep:
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

def durban():
    '''
    Index of Durban:
    http://www2.nilu.no/airquality/
    '''

    url = 'http://www2.nilu.no/airquality/'
    soup = BeautifulSoup(requests.get(url).content)

    span = soup.find('span', {'class': 'head1'})
    span_value = span.next
    city_name = span_value.split(' ')[-1]

    bolds = soup.findAll('b')
    index = bolds[1].next

    return {slugify(city_name):(city_name, index)}

def hong_kong():
    '''
    Index of Hong Kong:
    http://www.epd-asg.gov.hk/
    '''
    
    url = 'http://www.epd-asg.gov.hk/'
    soup = BeautifulSoup(requests.get(url).content)
    a = soup.find('a', {'href': '/english/backgd/Central.html'})
    index = a.next.next.next.next.next.next
    city_name = u'Hong Kong'
    return {slugify(city_name):(city_name, index)}

def sydney():
    '''
    Indexes of Sydney:
    http://airquality.environment.nsw.gov.au/aquisnetnswphp/getPage.php?reportid=3
    '''

    url = 'http://airquality.environment.nsw.gov.au/aquisnetnswphp/getPage.php?reportid=3'
    soup = BeautifulSoup(requests.get(url).content)
    tds = soup.findAll('td', {'class':'region'})
    indexes = {}

    for td in tds:
        index = td.findNext('td', {'rowspan':re.compile('\d'), 'class':re.compile('\w')}).next
        region = td.next
        indexes[slugify(region)] = (region, index)
    
    return indexes

if __name__ == '__main__':
    d_indexes = air_now()
