import time
from selenium import webdriver
# from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
import json
import pandas as pd
import numpy as np
import random
import string

def getInitialReviews(aotyPages):
    music_reviews = {'artist': [], 'album_name': [], 'critic_score': [], 'link': []}
    
    Pitchfork_pages = np.arange(1, aotyPages)

    for page in tqdm(Pitchfork_pages):
        time.sleep(5)
        options = Options()
        driver = webdriver.Chrome(options=options)
        driver.get('https://www.albumoftheyear.org/publication/48-now-magazine/reviews/' + str(page) + '/')
        artists = driver.find_elements_by_class_name('artistTitle')
        album_titles = driver.find_elements_by_class_name('albumTitle')
        ratings = driver.find_elements_by_class_name('rating')
        links = driver.find_elements_by_class_name('ratingText')

        for artist in artists:
            music_reviews['artist'].append(artist.text)
        for album_title in album_titles:
            music_reviews['album_name'].append(album_title.text)
        for rating in ratings:
            music_reviews['critic_score'].append(int(rating.text) / 10)
        for link in links:
            final_link = link.find_element_by_css_selector('a').get_attribute('href')
            music_reviews['link'].append(final_link)
        
        driver.quit()
    
    AOTY_Reviews = pd.DataFrame(music_reviews, columns=['artist', 'album_name', 'critic_score', 'link'])
    return AOTY_Reviews

data = getInitialReviews(62)
data.to_csv('nowToronto.csv')