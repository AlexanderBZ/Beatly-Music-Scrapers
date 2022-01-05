import requests
import json
import csv
import time
import math
import pandas as pd
import numpy as np
from tqdm import tqdm

def postReviews(review_data, critic_name):
    print("Deploying reviews")
    row_count = 0

    for col in review_data.index:
        row_count += 1

    for row in tqdm(range(row_count)):
        time.sleep(.5)


        album_name, artist, quote, link, critic_score = review_data.iloc[row]['album_name'], review_data.iloc[row]['artist'], review_data.iloc[row]['quote'], review_data.iloc[row]['link'], review_data.iloc[row]['critic_score'] 
        #album_name = album_name.replace("'", "’")
        critic_photo = f'https://media.beatlymusic.com/{critic_name.replace(" ", "").lower()}.jpg'

        try:
            payload = {
                "album_name": album_name,
                'artist': artist,
                'critic_name': critic_name,
                'critic_photo': critic_photo,
                'quote': quote,
                'review_link': link,
                "critic_score": round(float(critic_score)),
            }
            
            response = requests.post('https://63zrqq4iqb.execute-api.us-east-1.amazonaws.com/prod/criticreview',
                                              json=payload)
        except:
            continue