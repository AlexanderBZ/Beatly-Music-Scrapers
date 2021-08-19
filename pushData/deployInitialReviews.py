import requests
import json
import csv
import time
import math
import pandas as pd
import numpy as np
from tqdm import tqdm

def postReviewData(beatly_data):
    print("Deploying reviews")
    beatly_data = beatly_data[beatly_data.album_cover != 'NAP']

    row_count = 0

    for col in beatly_data.index:
        row_count += 1

    for row in tqdm(range(row_count)):
        time.sleep(.5)

        album_name, artist, pitchfork_score, pitchfork_qoute, pitchfork_link, sputnik_score, sputnik_qoute, sputnik_link = beatly_data.iloc[row]['album_name'], beatly_data.iloc[row]['artist'], beatly_data.iloc[row]['pitchfork_score'], beatly_data.iloc[row]['pitchfork_qoute'], beatly_data.iloc[row]['pitchfork_link'], beatly_data.iloc[row]['sputnik_score'], beatly_data.iloc[row]['sputnik_qoute'], beatly_data.iloc[row]['sputnik_link']

        try:
            payload = {
                "album_name": album_name,
                'artist': artist,
                'critic_name': 'Pitchfork',
                'critic_photo': 'https://media.beatlymusic.com/pitchfork.jpg',
                'quote': pitchfork_qoute,
                'review_link': pitchfork_link,
                "critic_score": round(float(pitchfork_score)),
            }
            
            response = requests.post('https://63zrqq4iqb.execute-api.us-east-1.amazonaws.com/prod/criticreview',
                                              json=payload)
        except:
            continue

        try:
            payload = {
                "album_name": album_name,
                'artist': artist,
                'critic_name': 'Sputnik Music',
                'critic_photo': 'https://media.beatlymusic.com/sputnikmusic.jpg',
                'quote': sputnik_qoute,
                'review_link': sputnik_link,
                "critic_score": round(float(sputnik_score)),
            }
            
            response = requests.post('https://63zrqq4iqb.execute-api.us-east-1.amazonaws.com/prod/criticreview',
                                              json=payload)
        except:
            continue
