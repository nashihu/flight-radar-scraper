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


browser = webdriver.Chrome('/Users/ahmad/Desktop/chromedriver')
browser.get("https://www.flightradar24.com/data/airports/bdo/arrivals")


int(input("pencet btn 'Load earlieur flights' yud abis itu type any int to continue: "))
    

#int(input("press any int when page is loaded to continue: "))
offset = parser.parse('9:50 AM')

#sip = browser.find_element_by_tag_name('td')

waktu = browser.find_elements_by_class_name('ng-binding')
css = browser.find_elements_by_css_selector('tr[data-date^="Monday, Feb 03"]')
pesawat = browser.find_elements_by_class_name('hide-mobile-only.ng-binding')
flightC = browser.find_elements_by_class_name('p-l-s.cell-flight-number')
codeArea = browser.find_elements_by_class_name('fs-10.fbold.notranslate.ng-binding')
asdf
waktus = list(filter(lambda x: (len(x.text)==8  or len(x.text)==7) 
                           and (x.text.find('AM')>-1 or (x.text.find('PM')>-1)), waktu))
codeArea = list(filter(lambda x: len(x.text)<6 and len(x.text)>0,codeArea))
waktus.pop(0)
for i in range(len(waktus)):
    try:
        int(waktus[i].text[0])
    except ValueError:
        waktus.pop(i)
    except IndexError:
        continue
#if(len(waktus) == len(pesawat)):
for i in range(len(waktus)):
    try:
        print('{} {} {} {}'.format((codeArea[i].text),(pesawat[i].text),(flightC[i].text),(waktus[i].text)))
        x=1
    except:
        print('exception time: {}'.format(waktus[i].text))

timez = list(map(lambda x: parser.parse(x.text),waktus))
delta = list(map(lambda x: ((x - offset).seconds)/3600, timez))
size = len(waktus)
codeArea = list(map(lambda x: x.text, codeArea[0:size]))
pesawat = list(map(lambda x: x.text, pesawat[0:size]))
flightC = list(map(lambda x: x.text, flightC[0:size]))
timez = timez[0:size]
delta = delta[0:size]
df = pd.DataFrame({'area':codeArea,'zone':pesawat,'flightC':flightC,'time':timez, 'delta':delta})
print('')
print('before')
print(df.head())
df2 = df[df['delta'] > 1.0][ df['delta'] < 3.0]
print('')
print('after')
print(df2)
#else:
#    print('len ga sama wk: waktu: {} pesawat: {}'.format((len(waktus)),(len(pesawat))))
        
#for i in range(len(codeArea)):
#    print(codeArea[i].text)