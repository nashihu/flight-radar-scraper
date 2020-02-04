#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 21:56:14 2020

@author: ahmad
"""

from selenium import webdriver
import time
import pandas as pd
from dateutil import parser

jamber = '9:50 AM'
offset = parser.parse(jamber)
getDataBeforeArrival = True
airportCode = 'bdo'

browser = webdriver.Chrome('./chromedriver')
browser.get("https://www.flightradar24.com/data/airports/{}/arrivals".format(airportCode))

int(input("pencet btn 'Load earlieur flights' yud abis itu type any int to continue: "))
    
css = browser.find_elements_by_css_selector('tr[data-date^="Monday, Feb 03"]')
print('found {} data'.format(len(css)))
print('mapping times')
timez = list(map(lambda x: x.find_elements_by_class_name('ng-binding')[0].text, css))
print('mapping flight number')
flightC = list(map(lambda x: x.find_elements_by_class_name('ng-binding')[1].text, css))
print('mapping origin')
pesawat = list(map(lambda x: x.find_elements_by_class_name('ng-binding')[2].text, css))
print('mapping code area')
codeArea = list(map(lambda x: x.find_elements_by_class_name('ng-binding')[3].text, css))
print('mapping landing status')
status = list(map(lambda x: x.find_elements_by_class_name('ng-binding')[7].text, css))
print('converting times')
timez = list(map(lambda x: parser.parse(x),timez))
print('calculating deltas')
delta = list(map(lambda x: ((x - offset).seconds)/3600, timez))
jamber = jamber.replace(':','.')
ext = 'departure'
if(getDataBeforeArrival) :
    ext = 'arrival'
    delta = list(map(lambda x: ((offset - x).seconds)/3600, timez))
timez = list(map(lambda x: x.strftime('%H:%M'), timez))
df = pd.DataFrame({'area':codeArea,
                   'zone':pesawat,
                   'flightC':flightC,
                   'time':timez, 
                   'delta':delta,
                   'status':status})
#df = df[df['status'] != 'Unknown'].reset_index(drop=True)
print('')
print('before')
print(df.head())
df2 = df[df['delta'] > 1.0][ df['delta'] < 3.0].reset_index(drop=True)
df2['delta'] = list(map(lambda x: parser.parse('{}:{}'.format(str(x)[0],
   (int(float(str(x)[1:4])*60)))).strftime('%H:%M') ,
    df2['delta'].tolist()))
df2 = df2.sort_values(by='status')
print('')
print('after')
print(df2)

writer = pd.ExcelWriter('{} - {} - {}.xlsx'.format(airportCode,ext,jamber))  
df2.to_excel(writer,'mantap')
writer.save()
#









