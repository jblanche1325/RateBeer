#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import pandas as pd

data_files = [f for f in os.listdir() if 'beer_table' in f]

for file in data_files:
    beer_file = pd.read_csv(file, header=0)
    big_beer_table.append(beer_file)
    
beer_df = pd.concat(big_beer_table, axis=0, ignore_index=True)

beer_df.to_csv('beer_df.csv', index=False)

