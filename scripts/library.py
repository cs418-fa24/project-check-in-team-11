# import json

# import spotipy
# from spotipy.oauth2 import SpotifyOAuth

# CLIENT_ID = ''
# CLIENT_SECRET = ''
# REDIRECT_URI = 'http://localhost:8888/callback'

# moods = {
#     'HAPPY': '37i9dQZF1EVJSvZp5AOML2',
#     'SAD': '37i9dQZF1EIh4v230xvJvd',
#     'CHILL': '37i9dQZF1EIdNTvkcjcOzJ',
#     'ENERGETIC': '37i9dQZF1EIcVDa7Tg8a0MY'
# }

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
#     client_id=CLIENT_ID,
#     client_secret=CLIENT_SECRET,
#     redirect_uri=REDIRECT_URI,
#     scope="playlist-read-private user-library-read"  # now accessing private user playlists
# ))

# sp1 = spotipy.Spotify(auth_manager=SpotifyOAuth(
#     client_id=CLIENT_ID,
#     client_secret=CLIENT_SECRET,
#     redirect_uri=REDIRECT_URI,
#     scope="playlist-read-private user-library-read"  # now accessing private user playlists
# ))


# # Get the user's liked songs
# results = sp.current_user_saved_tracks()
# liked_songs = []

# while results:
#     for item in results['items']:
#         track = item['track']
#         features = sp1.audio_features(track['id'])[0]
#         liked_songs.append({
#             'name': track['name'],
#             'id': track['id'],
#             'acousticness': features['acousticness'],
#             'danceability': features['danceability'],
#             'duration_ms': features['duration_ms'],
#             'energy': features['energy'],
#             'instrumentalness': features['instrumentalness'],
#             'key': features['key'],
#             'liveness': features['liveness'],
#             'loudness': features['loudness'],
#             'mode': features['mode'],
#             'speechiness': features['speechiness'],
#             'tempo': features['tempo'],
#             'time_signature': features['time_signature'],
#             'valence': features['valence']
#         })

#     results = sp.next(results)

# #TODO change the number so you know which files are yours
# num = 5
# with open(f'../raw/liked_songs_{num}.json', 'w') as json_file:
#     json.dump(liked_songs, json_file, indent=4)

import json
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'http://localhost:8888/callback'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-library-read"
))
results = sp.current_user_saved_tracks(limit=50)
liked_songs = []
count = 0  # To keep track of songs fetched

while results and count < 500:
    for item in results['items']:
        track = item['track']
        try:
            features = sp.audio_features(track['id'])[0]
            liked_songs.append({
                'name': track['name'],
                'id': track['id'],
                'acousticness': features['acousticness'],
                'danceability': features['danceability'],
                'duration_ms': features['duration_ms'],
                'energy': features['energy'],
                'instrumentalness': features['instrumentalness'],
                'key': features['key'],
                'liveness': features['liveness'],
                'loudness': features['loudness'],
                'mode': features['mode'],
                'speechiness': features['speechiness'],
                'tempo': features['tempo'],
                'time_signature': features['time_signature'],
                'valence': features['valence']
            })
            count += 1
            if count >= 500:
                break
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 429:
                retry_after = int(e.headers['Retry-After'])
                time.sleep(retry_after + 1)  # Sleep and retry after the time specified in the header
            else:
                raise e

    if count < 500:
        results = sp.next(results)
num = 5
with open(f'../raw/liked_songs_{num}.json', 'w') as json_file:
    json.dump(liked_songs, json_file, indent=4)
