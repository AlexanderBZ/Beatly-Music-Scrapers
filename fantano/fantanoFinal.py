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
from tqdm import tqdm
from fantano import fantanoInitial

#32
def getFinalReviews():
    print("Getting initial Fantano reviews")
    fantano_data = fantanoInitial.getInitialReviews()

    print("Getting Final Fatano reviews")
    fantano_reviews = {'album_name': [], 'artist': [], 'critic_photo': [], 'critic_score': [], 'link': [], 'quote': []}
    options = Options()
    driver = webdriver.Chrome(options=options)

    # Find number of rows in dataframe index
    row_count = 0

    for col in fantano_data.index:
        row_count += 1

    for row in tqdm(range(row_count)):
        driver.get(fantano_data.loc[row]["link"])

        title = driver.find_elements_by_class_name('entry-title')[0]
        finalTitle = title.find_element_by_css_selector('a').text

        youtubeVideo = driver.find_elements_by_class_name('fluid-width-video-wrapper')[0]
        youtubeLink = youtubeVideo.find_element_by_css_selector('iframe').get_attribute('src')

        excerpt = driver.find_elements_by_class_name('sqs-block-content')[1]
        quote = excerpt.find_element_by_css_selector('p').text

        entryTags = driver.find_elements_by_class_name('entry-tags')[0]
        hrefs = entryTags.find_elements_by_css_selector('a')

        for href in hrefs:
            if "/" in href.text:
                score = int(href.text[0])


        artist_end = finalTitle.index(' -')
        artist = finalTitle[0:artist_end]
        title_start = finalTitle.index('-') + 2
        album_name = finalTitle[title_start:] 


        fantano_reviews['album_name'].append(album_name)
        fantano_reviews['artist'].append(artist)
        fantano_reviews['critic_photo'].append("https://media.beatlymusic.com/theneedledrop.jpg")
        fantano_reviews['critic_score'].append(score)
        fantano_reviews['link'].append(youtubeLink)
        fantano_reviews['quote'].append(quote.strip())

    Fantano_Reviews = pd.DataFrame(fantano_reviews, columns=['album_name', 'artist', 'critic_photo', 'critic_score', 'link', 'quote'])
    driver.quit()
    return Fantano_Reviews