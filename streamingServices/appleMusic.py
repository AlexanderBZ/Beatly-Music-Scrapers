import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import numpy as np
import time
import json
import sys
import random
import requests_cache

def getAppleMusicData(beatly_data, appleMusicToken):
    print("Scraping the Apple Music IDs now")

    bearerToken = 'Bearer ' + str(appleMusicToken)

    appleMusic_data = {'appleMusicID': [], 'album_name': [], 'genres': [], 'release_date': []}

    # Find number of rows in dataframe index
    row_count = 0

    for col in beatly_data.index:
        row_count += 1

    session = requests_cache.CachedSession('appleMusicCache')
    # visit each link and find ID
    for row in tqdm(range(row_count)):
        searchTermFormatted = ""
        searchTerm = str(beatly_data.loc[row]["album_name"] + " " + beatly_data.loc[row]["artist"])

        #searchTerm =
        for letter in searchTerm:
            if letter == " ":
                searchTermFormatted += "+"
            else:
                searchTermFormatted += str(letter)

        query = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': bearerToken}
        requestURL = session.get("https://api.music.apple.com/v1/catalog/us/search?term=" + searchTermFormatted + '&limit=1&types=albums', headers=query).text

        time.sleep(1)

        if requestURL:
            requestDict = json.loads(requestURL)
            try:
                results = requestDict["results"]
                albums = results["albums"]
                data = albums['data']
                appleMusicID = data[0]["id"]
                appleMusic_data['appleMusicID'].append(appleMusicID)
                appleMusic_data['album_name'].append(str(beatly_data.loc[row]["album_name"]))
                attributes = data[0]["attributes"]
                genres = attributes['genreNames']
                date = attributes['releaseDate']
                appleMusic_data['genres'].append(genres)
                appleMusic_data['release_date'].append(date)
            except:
                appleMusic_data['appleMusicID'].append("nap")
                appleMusic_data['genres'].append(['nap'])
                appleMusic_data['release_date'].append(['nap'])
                appleMusic_data['album_name'].append(str(beatly_data.loc[row]["album_name"]))

    Final_AppleMusic = pd.DataFrame(appleMusic_data, columns=['album_name', 'appleMusicID', 'genres', 'release_date'])
    apple_beatly_data = pd.merge(beatly_data, Final_AppleMusic, on="album_name")
    return apple_beatly_data