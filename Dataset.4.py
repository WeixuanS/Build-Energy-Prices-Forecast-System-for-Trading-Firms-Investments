# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 14:28:12 2020

@author: Weixuan Sun
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import pandas as pd

html = urlopen('https://markets.businessinsider.com/commodities/historical-prices/natural-gas-price/usd')
dataset4_raw = BeautifulSoup(html.read(), "lxml")

fout = open('data4.txt', 'wt', encoding='utf-8')
fout.write(str(dataset4_raw))
fout.close()

dataset4_raw = str(dataset4_raw)
print(dataset4_raw)

data_index = dataset4_raw.find("data")

dataset4_raw = dataset4_raw[data_index + 8: -23]

dataset4_raw = dataset4_raw.split('],[')
print(dataset4_raw[0])
print(len(dataset4_raw)) 
temp = '[' + dataset4_raw[0] + ']'
temp_list = json.loads(temp)
print(temp_list)
print(type(temp_list))

res = [];
for i in range(len(dataset4_raw)):
    temp = '[' + dataset4_raw[i] + ']';
    temp_list = json.loads(temp);
    res.append(temp_list);
    
dataset4raw_df = pd.DataFrame(res) 
dataset4raw_df.to_excel("dataset3_raw.xlsx")

dataset4_clean = dataset4raw_df;
dataset4_clean.to_excel("dataset3_clean.xlsx")