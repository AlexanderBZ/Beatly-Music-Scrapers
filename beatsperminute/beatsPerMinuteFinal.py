import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import numpy as np
import time
from beatsperminute import beatsPerMinuteInitial
import random
import requests_cache

# Pitchfork Final Scores
def getFinalBeatsPerReviews(beatsPerPages):
    initial_BeatsPer = beatsPerMinuteInitial.getIntialBeatsPerReviews(beatsPerPages)
    print("Scraping the Final Beats Per Minute Reviews now")

    scores_data = {'album_name': [], 'artist': [], 'critic_photo': [], 'critic_score': [], 'link': [], 'quote': []}

    # Find number of rows in dataframe index
    row_count = 0

    for col in initial_BeatsPer.index:
        row_count += 1

    session = requests_cache.CachedSession('beatsPerFinalCache')
    # visit each link and find score
    for row in tqdm(range(row_count)):
        # request website
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
        website_url = session.get(initial_BeatsPer.loc[row]["link"], headers=headers).text

        # create soup of website
        soup = BeautifulSoup(website_url, 'lxml')
        counter = 0

        try:
            # find quote
            paragraph = soup.find('p')
            quote = paragraph.text

            # find rating
            score = soup.find('div', {'id': 'rating'})        

            # format quote 
            if len(paragraph.text) > 100:
                quote = paragraph.text.partition('.')[0] + '.'

            if len(quote) > 100:
                quote = quote[:100].rstrip() + '...'

            # format critic score
            formatedScore = int(score.find('h3').text[:-1]) / 10

            # append all attributes to 
            scores_data['critic_score'].append(formatedScore)
            scores_data['quote'].append(quote)
            scores_data['artist'].append(str(initial_BeatsPer.loc[row]["artist"]))
            scores_data['album_name'].append(str(initial_BeatsPer.loc[row]["album_name"]).strip())
            scores_data['link'].append(str(initial_BeatsPer.loc[row]["link"]))
            scores_data['critic_photo'].append("https://media.beatlymusic.com/beatsperminute.jpg")       
        except:
            counter += 1
        # find scores, images

    # create 2nd dataframe
    Final_BeatsPer = pd.DataFrame(scores_data, columns=['album_name', 'artist', 'critic_photo', 'critic_score', 'link', 'quote'])
    return Final_BeatsPer