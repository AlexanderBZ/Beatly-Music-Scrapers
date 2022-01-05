import requests
import json
import csv
import time
import pandas as pd
from tqdm import tqdm
import urllib3

with open('backup.csv', mode='r', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    counter = 0

    for row in tqdm(csv_reader):
        time.sleep(.5)

        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
            
        payload = {
            "album_name": row["album_name"].lower(),
            "artist": row["artist"].lower(),
            "album_cover": row["album_cover"],
        }

        response = requests.post('https://ji13d7wouf.execute-api.us-east-1.amazonaws.com/prod/updatealbum',
                                      json=payload)
        
        line_count += 1
    print(f'Processed {line_count} lines.')
