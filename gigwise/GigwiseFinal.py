import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import numpy as np
import time
import random
import requests_cache
from gigwise import AOTYScraperInitial

# Gigwise Final Scores
def getFinalGigwiseReviews():
    print("Scraping the Initial Gigwise Reviews now")
    initial_Gigwise = AOTYScraperInitial.getInitialReviews(1)

    print("Scraping the Final Gigwise Reviews now")

    music_reviews = {'album_name': [], 'artist': [], 'critic_photo': [], 'critic_score': [], 'link': [], 'quote': []}

    # Find number of rows in dataframe index
    row_count = 0

    for col in initial_Gigwise.index:
        row_count += 1

    session = requests_cache.CachedSession('gigwiseCache')
    # visit each link and find score
    for row in tqdm(range(row_count)):
        # request website
        # time.sleep(.5)

        headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
        website_url = session.get(initial_Gigwise.loc[row]["link"], headers=headers).text

        # create soup of website
        soup = BeautifulSoup(website_url, 'lxml')

        # find scores, images
        try: 
            left_side = soup.find('div', {'class': 'post_details'})
            excerpt = left_side.find('div', {'class': 'sub_title'})
            music_reviews['quote'].append(excerpt.text.strip())
            music_reviews['artist'].append(initial_Gigwise.loc[row]["artist"])
            music_reviews['album_name'].append(initial_Gigwise.loc[row]["album_name"])
            music_reviews['critic_photo'].append("https://media.beatlymusic.com/gigwise.jpg")
            music_reviews['critic_score'].append(initial_Gigwise.loc[row]["critic_score"])
            music_reviews['link'].append(initial_Gigwise.loc[row]["link"])
        except: 
            continue

    # create 2nd dataframe
    Final_Gigwise = pd.DataFrame(music_reviews, columns=['album_name', 'artist', 'critic_photo', 'critic_score', 'link', 'quote'])

    # combine 1st and 2nd dataframes
    return Final_Gigwise