# Beatly Music Scrapers

Welcome to the Music Scrapers repo for Beatly Music! The scrapers can be divided into two main groups. The album scrapers (which include things like Pitchfork, Apple Music, and LastFM scrapers) will scrape for album data and then push any new albums to the database. The reviews scrapers will then go through all the participating websites and get critic reviews to push to the database. See more information about the scrapers below.

## Usage

When you clone the repo you must do three main things before running it.

- Download the required javascript packages
- Activate the python env
- Get a Spotify API token
- Run the applemusic/appleMusicToken.js file to get an Apple Music token
- Then run the beatly_data.py file to push initial album data
- Finally, run the reviews_data.py to push critic reviews

## Album Scrapers

The album scrapers section can be divided into a couple of main parts:

- The beatly_data.py file is the only file that you have to run. This file runs the other files and merges any of the data received from the functions into one giant dataset. This is the file that outputs the final CSV file as well.
- The pitchforkFinal.py and sputnikFinal.py files run the initial scrapers which scrape the home pages for the reviews. The final scrapers then go into the unique URL of each album taken from the initial sweep and add any data that couldn't be gotten through the initial scrapes such as the review quotes.
- The appleMusic.py and spotify.py files send a request to the APIs of the two companies and then sort through the response to get streaming IDs and genres of the albums.
- The deployAlbum.py file is used to deploy the data to the Beatly database
- The lastFM.py and images.py files get and download album covers.

## Reviews Scrapers

This repo is quite simple. The scrapers go through all participating websites and get reviews.

- The GigwiseFinal.py scraper goes through AOTY to get the albums and then scrapes all the Gigwise links gotten from AOTY to get the reviews
- The FantanoFinal.py scraper uses selenium to scrape the needle drop website for reviews.
- The beatsPerMinute.py file goes through all the Beats Per Minute pages to get all the reviews from the website.
