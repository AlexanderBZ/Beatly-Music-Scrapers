import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import random
import pandas as pd
import numpy as np
import time
import requests_cache

# Pitchfork Initial
def getIntialPitchforkReviews(pitchforkPages):    
    print("Scraping the Initial Pitchfork Reviews now")

    # create empty lists to store everything in
    music_reviews = {'artist': [], 'album_name': [], 'pitchfork_link': []}

    # number of pages to scrape
    # total number of pages as of now are 1932
    Pitchfork_pages = np.arange(1, pitchforkPages)
    session = requests_cache.CachedSession('pitchforkInitialCache')

    # loop over given pages
    for page in tqdm(Pitchfork_pages):
        # request website
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
        website_url = session.get('https://pitchfork.com/reviews/albums/?page%20=&page=' + str(page), headers=headers).text
        #randomNumber = 1
        #time.sleep(randomNumber)

        # create soup of website
        soup = BeautifulSoup(website_url, 'lxml')

        # find all the attributes in table
        titles = soup.find_all('h2', {'class': "review__title-album"})
        musicians = soup.find_all('ul', {'class': "artist-list review__title-artist"})
        urls = soup.find_all('a', {'class': "review__link"})

        # add attributes to empty lists
        for title in titles:
            music_reviews['album_name'].append(title.text.title())

        for musician in musicians:
            music_reviews['artist'].append(musician.text.title())

        for url in urls:
            music_reviews['pitchfork_link'].append("http://pitchfork.com" + url.get('href'))
            
    # create 1st pandas data frame from full lists
    initial_Pitchfork = pd.DataFrame(music_reviews, columns=['artist', 'album_name', 'pitchfork_link'])
    return initial_Pitchfork  