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
def getInitialReviews():
    music_reviews = {'link': []}
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.theneedledrop.com/articles?category=Reviews')
    hrefs = driver.find_elements_by_class_name('entry-title')

    for href in hrefs:
        final_link = href.find_element_by_css_selector('a').get_attribute('href')
        music_reviews['link'].append(final_link)

    Fantano_Reviews = pd.DataFrame(music_reviews, columns=['link'])
    driver.quit()
    return Fantano_Reviews