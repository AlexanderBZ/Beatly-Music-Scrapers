import requests
import json
import csv
import time
import pandas as pd
from tqdm import tqdm
import urllib3

def postAlbumData(beatly_data):
    print("Deploying Albums")
    final_albums = {'album_name': [], 'artist': [], 'album_cover': [], 'genre': [], 'appleMusicID': [], 'spotifyID': [], 'date': [], 'slug': []}

    beatly_data = beatly_data[beatly_data.album_cover != 'NAP']

    row_count = 0

    for col in beatly_data.index:
        row_count += 1

    for row in tqdm(range(row_count)):
        time.sleep(2)

        album_name, artist, album_cover, appleMusicID, spotifyID, genres, release_date = beatly_data.iloc[row]['album_name'], beatly_data.iloc[row]['artist'], beatly_data.iloc[row]['album_cover'], beatly_data.iloc[row]['appleMusicID'], beatly_data.iloc[row]['spotifyID'], beatly_data.iloc[row]['genres'], beatly_data.iloc[row]['release_date']
        genres = genres[2:-2].split(', ')
        formattedGenres = []

        for genre in genres:
            formattedGenre = genre.replace('"', "").replace("'", "")
            if formattedGenre != "Music":
                formattedGenres.append(formattedGenre)

        payload = {
            "album_name": album_name,
            'artist': artist,
            'album_cover': album_cover,
            'genres': formattedGenres,
            'appleMusicID': appleMusicID,
            'spotifyID': spotifyID,
            "date": release_date
        }

        response = requests.post('https://ji13d7wouf.execute-api.us-east-1.amazonaws.com/prod/album',
                                              json=payload)

        if (response.status_code == 201):
            final_albums['album_name'].append(album_name)
            final_albums['artist'].append(artist)
            final_albums['album_cover'].append(album_cover)
            final_albums['appleMusicID'].append(appleMusicID)
            final_albums['spotifyID'].append(spotifyID)
            final_albums['genre'].append(genres)
            final_albums['date'].append(release_date)
            final_albums['slug'].append(json.loads(response.content)['slug'])
        else:
            print(response)

    Final_Reviews = pd.DataFrame(final_albums, columns=['album_name', 'artist', 'album_cover', 'genre', 'appleMusicID', 'spotifyID', 'date', 'slug'])
    Final_Reviews.to_csv('final_beatly_data.csv', index=False, encoding = 'utf-8-sig')
    return Final_Reviews
