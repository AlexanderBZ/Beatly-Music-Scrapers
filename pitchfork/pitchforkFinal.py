import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import numpy as np
import time
from pitchfork import pitchforkInitial
import random
import requests_cache

# Pitchfork Final Scores
def getFinalPitchforkReviews(pitchforkPages):
    initial_Pitchfork = pitchforkInitial.getIntialPitchforkReviews(pitchforkPages)
    print("Scraping the Final Pitchfork Reviews now")

    scores_data = {'pitchfork_score': [], 'album_cover': [], 'pitchfork_qoute': []}

    # Find number of rows in dataframe index
    row_count = 0

    for col in initial_Pitchfork.index:
        row_count += 1

    session = requests_cache.CachedSession('pitchforkFinalCache')
    # visit each link and find score
    for row in tqdm(range(row_count)):
        # request website
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
        website_url = session.get(initial_Pitchfork.loc[row]["pitchfork_link"], headers=headers).text
        time.sleep(2)

        # create soup of website
        soup = BeautifulSoup(website_url, 'lxml')

        # find scores, images
        ratings = soup.find('span', {'class': 'score'})
        artworkDiv = soup.find('div', {'class': 'single-album-tombstone__art'})
        qoute = soup.find('p')

        # add attributes to empty lists
        if ratings:
            scores_data['pitchfork_score'].append(float(ratings.text))
        else:
            scores_data['pitchfork_score'].append(int(7))

        if artworkDiv:
            artwork = artworkDiv.find('img')
            scores_data['album_cover'].append(artwork.get('src'))
        else:
            scores_data['album_cover'].append("NAP")

        if qoute:
            scores_data['pitchfork_qoute'].append(qoute.text)
        else:
            scores_data['pitchfork_qoute'].append("NAP")


    # create 2nd dataframe
    Final_Pitchfork = pd.DataFrame(scores_data, columns=['pitchfork_score', 'album_cover', 'pitchfork_qoute'])

    # combine 1st and 2nd dataframes
    horizontal_stack = pd.concat([initial_Pitchfork, Final_Pitchfork], axis=1)
    return horizontal_stack
