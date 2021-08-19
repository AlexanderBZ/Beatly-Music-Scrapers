import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import numpy as np
import time
import json
import sys
import requests_cache

def getSpotifyData(beatly_data, spotifyToken):
    # url for spotify api https://tinyurl.com/yn5ehehj
    print("Scraping the Spotify IDs now")

    # create bearer token from inputed spotify token
    bearerToken = 'Bearer ' + str(spotifyToken)

    # create empty list to store ID and album_name
    spotify_data = {'spotifyID': [], 'album_name': []}

    # Find number of rows in dataframe index
    row_count = 0

    # run loop to count how many rows in initial dataframe
    for col in beatly_data.index:
        row_count += 1

    session = requests_cache.CachedSession('lastFMCache')
    # visit each link and find ID
    for row in tqdm(range(row_count)):
        # format search term from album_name and artist
        searchTermFormatted = ""
        searchTerm = str(beatly_data.loc[row]["album_name"]) + " " + str(beatly_data.loc[row]["artist"])

        # replace spaces with "%20"
        for letter in searchTerm:
            if letter == " ":
                searchTermFormatted += "%20"
            else:
                searchTermFormatted += str(letter)

        # add query to request with bearer token
        query = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': bearerToken}
        requestURL = session.get("https://api.spotify.com/v1/search?q=" + searchTermFormatted + "&type=album&limit=1", headers=query).text

        # sleep in between requests
        time.sleep(1)

        # use try and except to append default data if regular function fails 
        try:
            requestDict = json.loads(requestURL)
            results = requestDict["albums"]
            results_Dictionary = results["items"]
            # isolate and append id from results_Dictionary
            id = results_Dictionary[0]["id"]
            spotify_data['spotifyID'].append(id)
            # append the album_name from the row
            spotify_data['album_name'].append(str(beatly_data.loc[row]["album_name"]))
        except:
            # append default data if any errors come up
            spotify_data['spotifyID'].append("nap")
            spotify_data['album_name'].append(str(beatly_data.loc[row]["album_name"]))

    # create pandas dataframe and merge data
    Final_Spotify = pd.DataFrame(spotify_data, columns=['album_name', 'spotifyID'])
    spotify_beatly_data = pd.merge(beatly_data, Final_Spotify, on="album_name")
    return spotify_beatly_data