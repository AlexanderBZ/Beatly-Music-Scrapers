import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import numpy as np
import time
import json
import sys
import uuid

def getImages(beatly_data):
    print("Downloading images now")

    imageNames = []

    # Find number of rows in dataframe index
    row_count = 0

    for col in beatly_data.index:
        row_count += 1

    # visit each link and find ID
    for row in tqdm(range(row_count)):
        time.sleep(.5)
        artistName = str(beatly_data.iloc[row]["artist"])


        searchTermFormatted = ''
        #searchTerm =
        for letter in artistName:
            if letter == " ":
                searchTermFormatted += "-"
            else:
                searchTermFormatted += str(letter)

        try:
            filename = f'{uuid.uuid4().hex}-300-{searchTermFormatted}.jpg'

            imageRequest = requests.get(beatly_data.iloc[row]["album_cover"])

            file = open(filename, "wb")
            file.write(imageRequest.content)
            file.close()  

            imageNames.append(filename)

        except:
            imageNames.append('NAP')


    del beatly_data['album_cover']
    beatly_data = beatly_data.assign(album_cover = imageNames)

    return beatly_data