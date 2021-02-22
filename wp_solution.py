#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import requests
import json
import math
from numpy import cos, sin, arcsin, sqrt
from math import radians
from datetime import datetime


def haversine(row):
    lon1 = 20.0
    lat1 = 52.0
    lat2 = row['latlng'][0]
    lon2 = row['latlng'][1]
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * arcsin(sqrt(a))
    km = 6367 * c
    return round(km, 3)


def is_in_eu(regionalBlocs):
    for block in regionalBlocs:
        if block['acronym'] == 'EU':
            return True
    return False


def country_languages(languages):
    c_l = []
    for language in languages:
        c_l.append(language['name'])

    return ', '.join(c_l)


def currency_codes(currencies):
    return currencies[0]['code']


def currency_symbols(currencies):
    return currencies[0]['symbol']


def timezones(timezones):
    return ', '.join(timezones)


def topLevelDomain(topLevelDomain):
    return ', '.join(topLevelDomain)


def rate_to_pln(currencyCode):
    get_value = requests.get(
        f'https://api.coinbase.com/v2/exchange-rates?currency={currencyCode}')
    get_value = get_value.json()
    return round(float(get_value['data']['rates']['PLN']), 3)


response = requests.get('https://restcountries.eu/rest/v2/region/europe')

eu_countries = response.json()


key_list = ['name', 'nativeName', 'numericCode', 'area', 'population', 'capital', 'languagesNames',
            'topLevelDomain', 'timezones', 'isEU', 'distanceToPl', 'currencySymbol', 'currencyCode', 'rateToPln', 'date']


for country in eu_countries:
    country['isEU'] = is_in_eu(country['regionalBlocs'])
    country['languagesNames'] = country_languages(country['languages'])
    country['currencyCode'] = currency_codes(country['currencies'])
    country['currencySymbol'] = currency_symbols(country['currencies'])
    country['distanceToPl'] = haversine(country)
    country['rateToPln'] = rate_to_pln(country['currencyCode'])
    country['date'] = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    country['timezones'] = timezones(country['timezones'])
    country['topLevelDomain'] = topLevelDomain(country['topLevelDomain'])

value_dict = {}
for i in range(len(eu_countries)):

    value_dict[i] = dict((k, eu_countries[i].get(k)) for k in (key_list))


df = pd.DataFrame.from_dict(value_dict)
df.transpose().to_csv('wp_report.csv')
