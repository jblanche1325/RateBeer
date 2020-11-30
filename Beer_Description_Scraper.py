#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup
import requests
import re
import sys

import pandas as pd

def get_beer_descriptions(base_url, beer_start, beer_end):
    
    beer_id_list = pd.read_csv('unique_beer_ids.csv')
    beer_id_list = beer_id_list['beer_id'][beer_start:beer_end].to_list()
    
    beer_path_name = ('beer_description_table_' + str(beer_start) + '_to_' + str(beer_end) + '.csv')
    unlisted_string = 'For one reason or another, this product is not thought to be suitable for reviewing.'
    
    beer_ids = []
    beer_descriptions = []
    
    for i in beer_id_list:
        page = requests.get(base_url + str(i))
        if page.ok:
            soup = BeautifulSoup(page.text, 'html.parser')
            if 'RETIRED' in soup.get_text().strip() or unlisted_string in soup.get_text().strip():
                pass
            else:
                # Beer ID
                beer_id = i
                beer_ids.append(beer_id)
                
                beer_description = soup.find('span', {'id': '_description3'})
                if beer_description is None:
                    beer_descriptions.append('No description')
                else:
                    try:
                        beer_description = soup.find('span', {'id': '_description3'}).get_text().strip().replace('\n', ' ')
                        beer_descriptions.append(beer_description)
                    except ValueError:
                        beer_descriptions.append('No description')
                
                print('iteration ' + str(i))
        else:
            pass
            print('iteration ' + str(i) + ': ' +  'Not Found')
        
    beer_descriptions_df = pd.DataFrame({'beer_id': beer_ids,
                                         'beer_description': beer_descriptions})

    beer_descriptions_df.to_csv(beer_path_name, index=False)

if __name__ == '__main__':
    beer_site = sys.argv[1]
    beer_start = int(sys.argv[2])
    beer_end = int(sys.argv[3])
    get_beer_descriptions(beer_site, beer_start, beer_end)
