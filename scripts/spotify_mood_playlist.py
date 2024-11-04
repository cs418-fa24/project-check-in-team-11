### Steps to get playlists ready to pull
# 1.) Find your mix playlists for each mood (happy, sad, energetic, chill)
# 2.) Click on the "..." and add to another playlist and create a new one. Spotify will create a default name "<mood> Mix (2)"
# 3.) Once you repeat this for all the moods, you are ready to use this script

import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# TODO insert info same as library.py...
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'http://localhost:8888/callback'

moods = {
    'HAPPY': '37i9dQZF1EVJSvZp5AOML2',
    'SAD': '37i9dQZF1EIh4v230xvJvd',
    'CHILL': '37i9dQZF1EIdNTvkcjcOzJ',
    'ENERGETIC': '37i9dQZF1EIcVD7Tg8a0MY'
}

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="playlist-read-private"  # now accessing private user playlists
))

sp1 = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="playlist-read-private"  # now accessing private user playlists
))

for mood, p_id in moods.items():
    results = sp.playlist_items(p_id)
    tracks = []

    while results:
        for item in results['items']:
            track = item['track']
            features = sp1.audio_features(track['id'])[0]

            if features is None:
                continue

            tracks.append({
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
        print("mood complete")
        # get next set of tracks
        results = sp.next(results)

    #TODO make sure to enter the number corresponding to your data
    num = 5
    with open(f'../raw/spotify_{mood.lower()}_{num}.json', 'w') as file:
        json.dump(tracks, file, indent=4)

    file.close()
