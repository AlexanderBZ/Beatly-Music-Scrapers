import time
from selenium import webdriver
# from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from bs4 import BeautifulSoup as bs
import json
import pandas as pd
import random
import string

#32
def getInitialReviews(real_page):
    music_reviews = {'artist': [], 'album_name': [], 'critic_score': [], 'link': []}
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.albumoftheyear.org/publication/71-gigwise/reviews/' + str(real_page) + '/')
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
        
    AOTY_Reviews = pd.DataFrame(music_reviews, columns=['artist', 'album_name', 'critic_score', 'link'])
    return AOTY_Reviews