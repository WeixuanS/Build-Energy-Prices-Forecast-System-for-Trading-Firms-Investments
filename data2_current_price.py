#!/usr/bin/env python
# coding: utf-8

# In[218]:


from urllib.request import urlopen
from bs4 import BeautifulSoup


# In[219]:


html = urlopen('https://markets.businessinsider.com/commodities/natural-gas-price')
bgas = BeautifulSoup(html.read(), "lxml")
fgas = open('gas_temp.txt', 'wt',
            encoding='utf-8')
fgas.write(str(bgas))
fgas.close()

gas_table_list = bgas.findAll('span',
                      { "class" : "push-data" } )
gas_table=gas_table_list[0]

for gas in gas_table.children:
    print(str(gas))


# In[220]:


html = urlopen('https://markets.businessinsider.com/commodities/oil-price?type=brent')
boil= BeautifulSoup(html.read(), "lxml")
foil = open('oil_temp.txt', 'wt',
            encoding='utf-8')
foil.write(str(boil))
foil.close()

oil_table_list = boil.findAll('span',
                      { "class" : "push-data" } )
oil_table=oil_table_list[0]

for oil in oil_table.children:
    print(str(oil))


# In[ ]:




