import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import numpy as np
import time
import json
import sys
import requests_cache

"""
<url>
  <loc>https://www.beatlymusic.com/news/how-rock-has-influenced-hip-hop</loc>
  <lastmod>2021-06-15T15:53:50+00:00</lastmod>
  <priority>0.64</priority>
</url>
"""

def getData():
    print("Scraping the data now")
    xml = []

    # open and get json from file
    

    with open('news.json') as fp:
        albums = json.load(fp)

    # loop through json and turn it into xml
    for album in albums:
        slug = album.get('slug')
        # skip over any album that has illegal XML characters
        if '&' in slug or "'s" in slug:
            continue 

        URL = f'<url>\n<loc>https://www.beatlymusic.com/album/{slug}</loc>  \n<lastmod>2021-06-15T15:53:50+00:00</lastmod>\n<priority>0.8</priority>\n</url>\n'
        xml.append(URL)
    
    # save XML to local file
    file1 = open("test.txt","w")
    file1.writelines(xml)