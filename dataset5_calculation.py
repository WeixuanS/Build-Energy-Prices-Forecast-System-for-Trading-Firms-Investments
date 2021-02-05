# -*- coding: utf-8 -*-
"""
Created on Fri Feb  20

@author: sheetalc
"""

import json
import requests
import pandas as pd

#API for Oil
response = requests.get("https://api.eia.gov/series/?api_key=bdc665fdd718f4f2624518fada5e39f8&series_id=EBA.US48-ALL.NG.OIL.H")
raw_data = json.loads(response.text)

temp_list = raw_data['series'][0]['data']

'''
Essentially the first element in the list will represent the recent most current date.
Hence taking the value for that and subtracting it with the 6th element
'''
change = temp_list[0][1] - temp_list[5][1]

#if change is negative put 0
if change > 0:
    changerPerForOil = change/temp_list[0][1]
else:
    changerPerForOil = 0

#API for Natural gas, repeat similar steps as for oil
response = requests.get("http://api.eia.gov/series/?api_key=bdc665fdd718f4f2624518fada5e39f8&series_id=EBA.US48-ALL.NG.NG.H")
raw_data = json.loads(response.text)

temp_list = raw_data['series'][0]['data']

change = temp_list[0][1] - temp_list[5][1]
if change > 0:
    changerPerForNG = change/temp_list[0][1]
else:
    changerPerForNG = 0

data = {'Type':['Oil', 'Natural Gas'],
        '% Change':[changerPerForOil,changerPerForNG ]} 

df = pd.DataFrame(data)

print(df)