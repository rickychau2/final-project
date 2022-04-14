import datetime

import requests
import csv
import re
from tqdm import tqdm
from urllib.parse import quote

CLIENT_ID = "e377c2362cad43548faf358203d63515"
CLIENT_SECRET = "d97c4f6b80bd4c5cb5b3f7a483d7bbb4"

AUTH_URL = "https://accounts.spotify.com/api/token"
BASE_URL = 'https://api.spotify.com/v1/'

def get_token():
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    # Convert response to JSON
    auth_response_data = auth_response.json()

    # Save the access token
    access_token = auth_response_data['access_token']
    return access_token

def clean(artists):
    delimitors = ' & |&|, |,| Featuring | X | / |/'
    return re.split(delimitors, artists)


def get_features(song, artist, access_token):
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    song = quote(song)
    artist = quote(artist)
    artist_1st = quote(clean(artist)[0])

    def get_song(song_name, artist_name):
        # GET song ID
        url = BASE_URL + f"search?q=track:{song_name}%20artist:{artist_name}&type=track&market=ES&limit=1"
        # url = BASE_URL + f"search?q={song_name}%20{artist_name}&type=track&market=ES&limit=1"
        r = requests.get(url, headers=headers)
        return r.json()

    r1 = get_song(song, artist)
    r2 = get_song(song, artist_1st)

    # what if no results are returned
    if len(r1['tracks']['items']) == 0:
        if len(r2['tracks']['items']) == 0:
            return []
        song_id = r2['tracks']['items'][0]['id']
    else:
        song_id = r1['tracks']['items'][0]['id']

    # GET song features
    url = BASE_URL + f"audio-features/{song_id}"
    r = requests.get(url, headers=headers)
    r = r.json()

    return list(r.values())


def write_features(decade):
    table_headers = ["song", "artist", "weeks_on_chart", "1st_appear"]
    spotify_features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms', 'time_signature']
    header = table_headers + spotify_features

    filename = 'billboard100/aggregate-by-decade/' + decade

    table = [header]
    placeholder = [""] * len(spotify_features)

    with open(filename, 'r') as f:
        next(f)  # skip the header
        reader = csv.reader(f)
        i = 0
        for row in tqdm(reader):
            if i % 100 == 0:
                access_token = get_token()
                print(access_token)

                with open('billboard100/song-features/' + decade + '_features', 'a') as f:
                    writer = csv.writer(f)
                    for datapoint in table:
                        writer.writerow(datapoint)
                    table = []
            song = row[0]
            artist = row[1]
            features = get_features(song, artist, access_token)
            if len(features) == 0:
                features = placeholder
            table.append(row + features)
            i += 1

    # with open('billboard100/songs-features/' + decade + '_features', 'w') as f:
    #     writer = csv.writer(f)
    #     for row in table:
    #         writer.writerow(row)


# date = datetime.date.fromisoformat('1970-01-03')
# end_date = datetime.date.today()
#
# while date < end_date:
#     print("processing..." + date.strftime("%Y-%m-%d"))
#     write_features(date.strftime("%Y-%m-%d"))
#     date = date + datetime.timedelta(7)

for decade in range(1970, 2030, 10):
    write_features(str(decade) + 's')