# -*- coding:utf-8 -*-
import re
import requests

from BeautifulSoup import BeautifulSoup


def slugify(value):
    # from Django
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import unicodedata
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)


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

    return {slugify(city_name): (city_name, index)}


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
    return {slugify(city_name): (city_name, index)}


def sydney():
    '''
    Indexes of Sydney:
    http://airquality.environment.nsw.gov.au/aquisnetnswphp/getPage.php?repor
    tid=3
    '''

    url = ('http://airquality.environment.nsw.gov.au/aquisnetnswphp/getPage.'
           'php?reportid=3')
    soup = BeautifulSoup(requests.get(url).content)
    tds = soup.findAll('td', {'class': 'region'})
    indexes = {}

    for td in tds:
        index = td.findNext(
                'td', {'rowspan': re.compile('\d'), 'class': re.compile('\w')}
            )
        index = index.next
        region = td.next
        indexes[slugify(region)] = (region, index)

    return indexes


def toronto():
    '''
    TODO: Get all indices of Ontario
    http://www.airqualityontario.com/reports/summary.php
    Index of Toronto:
    http://www.airqualityontario.com/reports/today.php?sites=31103
    '''
    url = 'http://www.airqualityontario.com/reports/today.php?sites=31103'
    soup = BeautifulSoup(requests.get(url).content)

    index = soup.findAll('p')[2].getText()
    index = re.search(r'\d+', index).group()

    return {'toronto': ('Toronto', index)}


def san_juan():
    '''
    San Juan
    http://www.prtc.net/%7Ejcaaqs/indice/indice.html
    '''
    url = 'http://www.prtc.net/~jcaagua/computoaire.htm'  # iframe
    soup = BeautifulSoup(requests.get(url).content)
    index = soup.findAll('td')[3].getText()
    return {'san-juan': ('San Juan', index)}


def air_quality():
    '''
    All indexes of airqualitynow.eu
    http://www.airqualitynow.eu/comparing_home.php
    '''
    url = 'http://www.airqualitynow.eu/comparing_home.php'
    soup = BeautifulSoup(requests.get(url).content)
    cities_tds = soup.findAll('td', {'class': re.compile('city_bkg\d+')})

    indexes = {}
    for td in cities_tds:
        index = td.parent.findAll('td')[-1]  # background index: now

        # Some kind of standart, empty string for null values
        index = index.getText().replace('-', '')

        indexes[slugify(td.getText())] = (td.getText(), index)

    return indexes


def lisbon():
    '''
    Lisbon
    http://www.qualar.org/INDEX.PHP?page=1&subzona=4
    '''
    url = 'http://www.qualar.org/INDEX.PHP?page=1&subzona=4'
    soup = BeautifulSoup(requests.get(url).content)
    td_base = soup.find('td', {'bgcolor': '#434343'})
    index = td_base.parent.parent.find('center').getText()
    return {'lisbon': ('Lisbon', index)}


def guimaraes():
    '''
    Guimarães
    http://www.qualar.org/INDEX.PHP?page=1&zona=141
    '''
    url = 'http://www.qualar.org/INDEX.PHP?page=1&zona=141'
    soup = BeautifulSoup(requests.get(url).content)
    td_base = soup.find('td', {'bgcolor': '#434343'})
    index = td_base.parent.parent.find('center').getText()
    return {'guimaraes': (u'Guimarães', index)}


if __name__ == '__main__':
    d_indexes = air_now()
