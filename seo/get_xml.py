import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import numpy as np
import time
import json
import sys
import requests_cache
from datetime import date
import csv

"""
<url>
  <loc>https://www.beatlymusic.com/news/how-rock-has-influenced-hip-hop</loc>
  <lastmod>2021-06-15T15:53:50+00:00</lastmod>
  <priority>0.64</priority>
</url>
"""

def getData(beatly_data):
    print("Scraping the data now")
    xml = []

    # Find number of rows in dataframe index
    row_count = 0

    for col in beatly_data.index:
        row_count += 1    

    for row in range(row_count):
        slug = beatly_data.loc[row]['slug']
        # skip over any album that has illegal XML characters
        if '&' in slug or "'s" in slug:
            continue 

        URL = f'<url>\n<loc>https://www.beatlymusic.com/album/{slug}</loc>  \n<lastmod>{date.today()}</lastmod>\n<priority>0.8</priority>\n</url>\n'
        xml.append(URL)
    
    # save XML to local file
    file1 = open("beatly_data.xml","a")
    file1.writelines(xml)

getData(pd.read_csv('beatly_data_initial.csv'))