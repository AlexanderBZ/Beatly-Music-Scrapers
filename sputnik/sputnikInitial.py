import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import numpy as np
import time
import requests_cache

# Sputnik Scrape
def getInitialSputnikReviews(sputnikPages):
    print("Scraping the Initial Sputnik Reviews now")

    # create empty lists to store everything in
    music_reviews = {'sputnik_link': [], 'artist': [], 'album_name': [], 'sputnik_score': []}

    # total number of pages as of now is 181
    Sputnik_pages = np.arange(1, sputnikPages)
    session = requests_cache.CachedSession('sputnikInitalCache')

    # create loop
    for page in tqdm(Sputnik_pages):
        # request website
        website_url = session.get('https://www.sputnikmusic.com/reviews/albums/' + str(page)).text
        #time.sleep(.5)
        
        # create soup of website
        soup = BeautifulSoup(website_url, 'lxml')

        # isolate table
        review_table = soup.find('table', {'cellpadding': 10}).find_all('tr')[2]

        # find all the attributes in table
        urls = review_table.find_all('a', href=True)
        musicians = review_table.find_all('b')
        titles = review_table.find_all('font', {'color': '#333333'})
        ratings = review_table.find_all('font', {'color': '#FF0000'})

        # add attributes to empty lists
        for url in urls:
            if url.text and '/user/' not in url['href']: 
                music_reviews['sputnik_link'].append("https://www.sputnikmusic.com" + url['href'])

        for musician in musicians:
            if musician.text.title() != 'Notice' and musician.text.title() != '/Var/Www/Html/Sputnik/Staffreviews.Php' and musician.text.title() != '54':
                music_reviews['artist'].append(musician.text.title())

        for title in titles:
            music_reviews['album_name'].append(title.text.title())

        for rating in ratings:
            music_reviews['sputnik_score'].append(float(rating.text) * 2)

    # create 3rd pandas data frame from full lists
    Sputnik_Reviews = pd.DataFrame(music_reviews, columns=['sputnik_link', 'artist', 'album_name', 'sputnik_score'])
    return Sputnik_Reviews