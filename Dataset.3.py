# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 12:43:53 2020

@author: Weixuan Sun
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import pandas as pd

html = urlopen('https://markets.businessinsider.com/commodities/historical-prices/oil-price/usd?type=wti')
dataset3_raw = BeautifulSoup(html.read(), "lxml")

fout = open('data3.txt', 'wt', encoding='utf-8')
fout.write(str(dataset3_raw))
fout.close()

dataset3_raw = str(dataset3_raw)
print(dataset3_raw)

data_index = dataset3_raw.find("data")

dataset3_raw = dataset3_raw[data_index + 8: -23]

dataset3_raw = dataset3_raw.split('],[')
print(dataset3_raw[0])
print(len(dataset3_raw)) 
temp = '[' + dataset3_raw[0] + ']'
temp_list = json.loads(temp)
print(temp_list)
print(type(temp_list))

res = [];
for i in range(len(dataset3_raw)):
    temp = '[' + dataset3_raw[i] + ']';
    temp_list = json.loads(temp);
    res.append(temp_list);
    
dataset3raw_df = pd.DataFrame(res) 
dataset3raw_df.to_excel("dataset3_raw.xlsx")

dataset3_clean = dataset3raw_df;
dataset3_clean.to_excel("dataset3_clean.xlsx")