# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 15:48:15 2020

@author: sheetalc
"""

import json
import requests

response = requests.get("https://api.eia.gov/series/?api_key=bdc665fdd718f4f2624518fada5e39f8&series_id=EBA.US48-ALL.NG.OIL.H")
raw_data = json.loads(response.text)
output_file_raw = open("dataset5_raw.txt", 'wt', encoding="UTF-8")
output_file_clean = open("dataset5.txt", 'wt', encoding="UTF-8")

output_file_raw.flush()
output_file_clean.flush()

output_file_raw.write("%s" %raw_data)

temp_list = raw_data['series'][0]['data']
#length = len(temp_list) 
#print(temp_list)

#data = [sub[0] for sub in temp_list]
#count = 0
output_file_clean.write("{:<10}{:<10}{:<10}".format("Date","Time","Value"))
output_file_clean.write("\n")
for data in temp_list:
    output_file_clean.write("{:<10}{:<10}{:<10}".format(data[0][:8], data[0][9:12], data[1]))
    output_file_clean.write("\n")
    #output_file_clean.write("%s\t%s" %data[0],%data[1])
    #count = count + 1
    
output_file_raw.close()
output_file_clean.close()