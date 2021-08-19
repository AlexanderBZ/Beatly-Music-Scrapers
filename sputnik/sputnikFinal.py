import requests
import re
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import numpy as np
import time
from sputnik import sputnikInitial
import requests_cache

# Pitchfork Final Scores
def getFinalSputnikReviews(sputnikPages):
    sputnikInitialData = sputnikInitial.getInitialSputnikReviews(sputnikPages)
    print("Scraping the Final Sputnik Reviews now")


    scores_data = {'sputnik_qoute': []}

    # Find number of rows in dataframe index
    row_count = 0

    for col in sputnikInitialData.index:
        row_count += 1

    session = requests_cache.CachedSession('sputnikFinalCache')

    # visit each link and find score
    for row in tqdm(range(row_count)):
        # request website
        website_url = session.get(sputnikInitialData.loc[row]["sputnik_link"]).text
        #time.sleep(.5)

        # create soup of website
        soup = BeautifulSoup(website_url, 'lxml')

        # isolate full review
        review_table = soup.find_all('table', {'width': '100%'})[1]
        review_table_data = review_table.find_all('tr')[4].find('td')
        articleDivs = review_table_data.find('div').find('div').find_all('div')[5]

        # find scores, images, and genres
        qouteDiv = articleDivs.find('div').text[16:]
        formattedQoute = qouteDiv.strip()

        scores_data['sputnik_qoute'].append(formattedQoute)

    # create 2nd dataframe
    sputnikFinalData = pd.DataFrame(scores_data, columns=['sputnik_qoute'])

    # combine 1st and 2nd dataframes
    horizontal_stack = pd.concat([sputnikInitialData, sputnikFinalData], axis=1)
    return horizontal_stack