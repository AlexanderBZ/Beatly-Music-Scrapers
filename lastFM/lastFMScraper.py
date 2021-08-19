import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import numpy as np
import time
import json
import sys
import requests_cache

def getlastFMData(beatly_data):
    print("Scraping the lastFM images now")
    
    lastFMToken = "aa4ce98160df5bbd096ff7bf83a27d35"

    # Find number of rows in dataframe index
    row_count = 0

    for col in beatly_data.index:
        row_count += 1

    # visit each link and find ID
    for row in tqdm(range(row_count)):
        searchTermFormatted = ""
        searchTerm = str(f'album={beatly_data.loc[row]["album_name"]}&artist={beatly_data.loc[row]["artist"]}')

        #searchTerm =
        for letter in searchTerm:
            if letter == " ":
                searchTermFormatted += "%20"
            else:
                searchTermFormatted += str(letter)

        session = requests_cache.CachedSession('lastFMCache')

        if pd.isnull(beatly_data.iloc[row]["album_cover"]):
            beatly_data.at[row, 'album_cover'] = "NAP"
        elif 'pitchfork' in beatly_data.iloc[row]["album_cover"]:
            continue
        else:
            try:
                query = {'Accept': 'application/json', 'Content-Type': 'application/json'}
                requestURL = session.get(f'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={lastFMToken}&{searchTermFormatted}&format=json', headers=query).text
                requestDict = json.loads(requestURL)
                result = requestDict["album"]
                images = result["image"]
                final_image = images[3]['#text']
                beatly_data.at[row, 'album_cover'] = final_image
                time.sleep(1.5)
            except:
                beatly_data.at[row, 'album_cover'] = "NAP"


    return beatly_data