from bs4 import BeautifulSoup
import requests
import re

import pandas as pd

def get_beer_ratings(base_url, beer_start, beer_end):
    
    beer_path_name = ('beer_table_' + str(beer_start) + '_to_' + str(beer_end) + '.csv')
    
    beer_ids = []
    beer_names = []
    beer_ratings = []
    #breweries = []
    brewery_ids = []
    styles = []
    rating_counts = []
    weighted_avgs = []
    calories = []
    abvs = []
    
    for i in range(beer_start, beer_end + 1):
        page = requests.get(base_beer_url + str(i))
        if page.ok:
            soup = BeautifulSoup(page.text, 'html.parser')
            if 'RETIRED' in soup.get_text().strip():
                pass
            else:
                # Beer ID
                beer_id = i
                beer_ids.append(beer_id)
                # Beer Name
                name = soup.find('div', class_='user-header').get_text().strip()
                beer_names.append(name)
                # Overall Rating
                rating = soup.find('div', class_='ratingValue')
                if rating is None:
                    beer_ratings.append(-1)
                else:
                    rating = soup.find('div', class_='ratingValue').get_text().strip()
                    beer_ratings.append(rating)
                # Brewery
                #brewery = soup.find('a', {'id': '_brand4'})
                #if brewery is None:
                 #   breweries.append('None')
                #else:
                 #   brewery = soup.find('a', {'id': '_brand4'}).get_text().strip()
                 #   breweries.append(brewery)
                # Brewery ID
                brewery_id = soup.find("a", href=re.compile('brewers'))
                if brewery_id is None:
                    brewery_ids.append('None')
                else:
                    try:
                        brewery_id = (soup.find("a", href=re.compile('brewers'))['href'].split('/', -1)[:-1])[-1]
                        brewery_ids.append(brewery_id)
                    except ValueError:
                        brewery_ids.append('None')
                # Style
                style = soup.find('span', {'id': 'styleTopFifty'})
                if style is None:
                    styles.append('None')
                else:
                    try:
                        style = soup.find('span', {'id': 'styleTopFifty'}).find_previous_sibling().get_text().strip()
                        styles.append(style)
                    except ValueError:
                        styles.append('None')
                # Number of Ratings
                rating_count = soup.find('span', {'id': '_ratingCount8'})
                if rating_count is None:
                    rating_counts.append(-1)
                else:
                    try:
                        rating_count = soup.find('span', {'id': '_ratingCount8'}).get_text().strip()
                        rating_counts.append(rating_count)
                    except ValueError:
                        rating_counts.append(-1)
                # Weighted Average of Ratings
                weighted_avg = soup.find('a', {'name': 'real average'})
                if weighted_avg is None:
                    weighted_avgs.append(-1)
                else:
                    try:
                        weighted_avg = float(soup.find('a', {'name': 'real average'}).get_text().split(":")[1].split('/')[0].strip())
                        weighted_avgs.append(weighted_avg)
                    except ValueError:
                        weighted_avgs.append(-1)
                # Calories
                cal = soup.find('abbr', {'title': 'Estimated calories for a 12 fluid ounce serving'})
                if cal is None:
                    calories.append(-1)
                else:
                    try:
                        cal = float(soup.find('abbr', {'title': 'Estimated calories for a 12 fluid ounce serving'}).find_next_sibling().get_text())
                        calories.append(cal)
                    except ValueError:
                        calories.append(-1)
                # ABV
                abv = soup.find('abbr', {'title': 'Alcohol By Volume'})
                if abv is None:
                    abvs.append(-1)
                else:
                    try:
                        abv = float(soup.find('abbr', {'title': 'Alcohol By Volume'}).find_next_sibling().get_text().rstrip('%'))
                        abvs.append(abv)
                    except ValueError:
                        abvs.append(-1)
                
                #print('iteration ' + str(i) + ': ' +  name)
        else:
            pass
            #print('iteration ' + str(i) + ': ' +  'Not Found')
        
    #global beer_info_df
    beer_info_df = pd.DataFrame({'beer_id': beer_ids,
                                 'beer_name': beer_names, 
                                 'overall_rating': beer_ratings, 
                                 #'brewery': breweries, 
                                 'brewery_id': brewery_ids,
                                 'style': styles, 
                                 'number_of_ratings': rating_counts,
                                 'weighted_avg_rating': weighted_avgs,
                                 'calories': calories,
                                 'abv': abvs})
    
    beer_info_df.to_csv(beer_path_name, index=False)
