import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import numpy as np
import time
import random
import requests_cache
#from gigwise import AOTYScraperInitial

# Gigwise Final Scores
def getFinalNotTorontoReviews():
    print("Scraping the Initial Now Toronto Reviews now")
    #initial_Gigwise = AOTYScraperInitial.getInitialReviews(1)
    initial_NowToronto = pd.read_csv('nowToronto.csv')

    print("Scraping the Final Now Toronto Reviews now")

    music_reviews = {'album_name': [], 'artist': [], 'critic_photo': [], 'critic_score': [], 'link': [], 'quote': []}

    # Find number of rows in dataframe index
    row_count = 0

    for col in initial_NowToronto.index:
        row_count += 1

    session = requests_cache.CachedSession('nowTorontoCache')
    # visit each link and find score
    # row_count
    for row in tqdm(range(1000)):
        time.sleep(0.1)


        # request website
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
        website_url = session.get(initial_NowToronto.loc[row]["link"], headers=headers).text

        # create soup of website
        soup = BeautifulSoup(website_url, 'lxml')

        # find scores, images
        try: 
            article = soup.find('div', {'class': 'post-inner'})
            excerpt = article.find('p')


            # format quote 
            if len(excerpt.text) > 120:
                quote = excerpt.text.partition('.')[0] + '.'

            if len(quote) > 120:
                quote = quote[:120].rstrip() + '...'
                
            music_reviews['quote'].append(quote.strip())
            music_reviews['artist'].append(initial_NowToronto.loc[row]["artist"])
            music_reviews['album_name'].append(initial_NowToronto.loc[row]["album_name"])
            music_reviews['critic_photo'].append("https://media.beatlymusic.com/nowtoronto.jpg")
            music_reviews['critic_score'].append(initial_NowToronto.loc[row]["critic_score"])
            music_reviews['link'].append(initial_NowToronto.loc[row]["link"])
        except: 
            continue

    # create 2nd dataframe
    Final_NowToronto = pd.DataFrame(music_reviews, columns=['album_name', 'artist', 'critic_photo', 'critic_score', 'link', 'quote'])

    # combine 1st and 2nd dataframes
    return Final_NowToronto

final = getFinalNotTorontoReviews()
final.to_csv('final.csv')