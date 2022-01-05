import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import numpy as np
import time
from vinylChapters import vinylChaptersInitial
import random
import requests_cache

# Pitchfork Final Scores
def getFinalVinylChaptersReviews(vinylChaptersPages):
    initial_VinylChapters = vinylChaptersInitial.getIntialVinylChaptersReviews(vinylChaptersPages)
    print("Scraping the Final Vinyl Chapters Reviews now")

    scores_data = {'album_name': [], 'artist': [], 'critic_photo': [], 'critic_score': [], 'link': [], 'quote': []}

    # Find number of rows in dataframe index
    row_count = 0

    for col in initial_VinylChapters.index:
        row_count += 1

    session = requests_cache.CachedSession('vinylChaptersFinalCache')
    # visit each link and find score
    for row in tqdm(range(row_count)):
        # request website
        time.sleep(.5)
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
        website_url = session.get(initial_VinylChapters.loc[row]["link"], headers=headers).text

        # create soup of website
        soup = BeautifulSoup(website_url, 'lxml')
        article = soup.find('div', {'class': "entry-content"})
        counter = 0

        try:
            # find quote
            paragraph = article.find('p')
            quote = paragraph.text

            # find rating
            score = article.find_all('p')[-1].text

            # format quote 
            if len(paragraph.text) > 120:
                quote = paragraph.text.partition('.')[0] + '.'

            if len(quote) > 120:
                quote = quote[:120].rstrip() + '...'

            # format critic score
            scoreIndex = score.index('/') - 1
            formatedScore = int(score[scoreIndex]) * 2


            # append all attributes to 
            scores_data['critic_score'].append(formatedScore)
            scores_data['quote'].append(quote)
            scores_data['artist'].append(str(initial_VinylChapters.loc[row]["artist"]))
            scores_data['album_name'].append(str(initial_VinylChapters.loc[row]["album_name"]).strip())
            scores_data['link'].append(str(initial_VinylChapters.loc[row]["link"]))
            scores_data['critic_photo'].append("https://media.beatlymusic.com/vinylchapters.jpg")       
        except:
            counter += 1
        # find scores, images

    # create 2nd dataframe
    Final_VinylChapters = pd.DataFrame(scores_data, columns=['album_name', 'artist', 'critic_photo', 'critic_score', 'link', 'quote'])
    return Final_VinylChapters

getFinalVinylChaptersReviews(153).to_csv("vinylChapters.csv")