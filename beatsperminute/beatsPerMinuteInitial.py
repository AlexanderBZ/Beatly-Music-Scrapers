import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import random
import pandas as pd
import numpy as np
import time
import requests_cache

# Beats Per Initial
def getIntialBeatsPerReviews(beatsPerPages):    
    print("Scraping the Initial Beats Per Minute Reviews now")

    # create empty lists to store everything in
    music_reviews = {'album_name': [], 'artist': [], 'link': []}

    # np.arange inputted pages
    BeatsPer_pages = np.arange(1, beatsPerPages)
    session = requests_cache.CachedSession('beatsPerInitialCache')

    # loop over given pages
    for page in tqdm(BeatsPer_pages):
        # request website
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
        website_url = session.get('https://beatsperminute.com/category/reviews/album-reviews/page/' + str(page) + '/', headers=headers).text

        # create soup of website
        soup = BeautifulSoup(website_url, 'lxml')

        # find all the attributes in table
        titles = soup.find_all('h2', {'class': "cb-post-title"})  
        counter = 0

        # add attributes to empty lists
        for title in titles:
            # get unformatted title
            unformattedTitle = title.text
            try:
                stringIndex = unformattedTitle.index('Album Review: ') + 14
                full_title = str(unformattedTitle[stringIndex:])
                # get artist title
                artist_end = full_title.index(' –') 
                # get album title
                title_start = full_title.index('–') + 2
                artist = full_title[0:artist_end]
                album_name = full_title[title_start:]
                # append all data to array
                music_reviews['artist'].append(artist)
                music_reviews['album_name'].append(album_name)
                music_reviews['link'].append(title.find('a')['href'])
            except Exception as e:
                counter += 1

            try:
                stringIndex = unformattedTitle.index('Album Review : ') + 15
                full_title = str(unformattedTitle[stringIndex:])
                # get artist title
                artist_end = full_title.index(' –') 
                # get album title
                title_start = full_title.index('–') + 2
                artist = full_title[0:artist_end]
                album_name = full_title[title_start:]
                # append all data to array
                music_reviews['artist'].append(artist)
                music_reviews['album_name'].append(album_name[:-12].strip())
                music_reviews['link'].append(title.find('a')['href'])
            except Exception as e:
                counter += 1

    # create 1st pandas data frame from list
    initial_BeatsPer = pd.DataFrame(music_reviews, columns=['album_name', 'artist', 'link'])
    return initial_BeatsPer