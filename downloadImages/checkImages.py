import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import numpy as np
import time
import json
import sys
import uuid

def checkImages(beatly_data):
    print("Checking images now")

    # Find number of rows in dataframe index
    row_count = 0

    for col in beatly_data.index:
        row_count += 1

    new_data = beatly_data

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
            requests.get(beatly_data.iloc[row]["album_cover"])
        except:
            new_data = beatly_data.drop(row)

    return new_data