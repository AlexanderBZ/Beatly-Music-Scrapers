import pandas as pd
import numpy as np
from pitchfork import pitchforkFinal
from sputnik import sputnikFinal
from streamingServices import appleMusic
from streamingServices import spotify
from lastFM import lastFMScraper
from downloadImages import images
from downloadImages import checkImages
from pushData import deployAlbum
from downloadImages import images
from pushData import deployInitialReviews
from seo import updateSeo

# ask how many pages should be scraped
print("How many Pitchfork Pages would you like to scrape today?")
pitchforkPages = int(input())

# ask how many pages should be scraped
print("How many Sputnik Pages would you like to scrape today?")
sputnikPages = int(input())

# ask for token
print("What is your apple music token?")
appleMusicToken = input()

# ask for token
print("What is your spotify token? https://tinyurl.com/yn5ehehj")
spotifyToken = input()

sputnik_reviews = sputnikFinal.getFinalSputnikReviews(sputnikPages)
pitchfork_reviews = pitchforkFinal.getFinalPitchforkReviews(pitchforkPages)

# Merge 2nd and 3rd dataframes
merged_data = pd.concat([sputnik_reviews, pitchfork_reviews], axis = 0, ignore_index=True)

# averageScore
beatly_data = merged_data.groupby(['album_name'], as_index=False).agg({'artist': 'first', 'pitchfork_score': 'first', 'pitchfork_qoute': 'first', 'pitchfork_link': 'first', 'sputnik_score': 'first', 'sputnik_qoute': 'first', 'sputnik_link': 'first', 'album_cover': 'first'})

# add additional columns
beatly_data["critic_score"] = 0
beatly_data["critic_number_of_ratings"] = 0
beatly_data["user_score"] = 0
beatly_data["user_number_of_ratings"] = 0

# get spotify data
beatly_data = spotify.getSpotifyData(beatly_data, spotifyToken)

# get apple music data
beatly_data = appleMusic.getAppleMusicData(beatly_data, appleMusicToken)

# get lastFM data
beatly_data = lastFMScraper.getlastFMData(beatly_data)

# remove any albums with no album cover
beatly_data = beatly_data[beatly_data['album_cover'].notnull()]

# check images
beatly_data = checkImages.checkImages(beatly_data)

# export to csv
beatly_data.to_csv('beatly_data.csv', index=False, encoding = 'utf-8-sig')

# deploy albums and reviews
final_data = deployAlbum.postAlbumData(pd.read_csv('beatly_data.csv'))
#deployInitialReviews.postReviewData(pd.read_csv('beatly_data.csv'))

updateSeo.updateSeo(final_data)

# download images
#images.getImages(final_data)