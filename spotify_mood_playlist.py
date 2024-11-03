### Steps to get playlists ready to pull
# 1.) Find your mix playlists for each mood (happy, sad, energetic, chill)
# 2.) Click on the "..." and add to another playlist and create a new one. Spotify will create a default name "<mood> Mix (2)"
# 3.) Once you repeat this for all the moods, you are ready to use this script

import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# TODO insert info same as library.py...
client_id = ''
client_secret = ''
redirect_uri = 'http://localhost:8888/callback'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="playlist-read-private" # now accessing private user playlists
))

# TODO insert playlist name we are pulling from (repeat for each mood)
playlist_name = 'ADD_NAME'
results = sp.current_user_playlists()

# Searching available playlists that match the playlist_name
while results:
    for item in results['items']:
        if item['name'] == playlist_name:
            playlist_id = item['id'] # find and assign the id
        
    # Get next batch of playlists
    results = sp.next(results)

# collecting all tracks and their ids from each playlist
tracks = []
results = sp.playlist_items(playlist_id)
    
while results:
    for item in results['items']:
        track = item['track']
        track_info = {
            'name': track['name'],
            'track_id': track['id']
        }
        tracks.append(track_info)
    
    # Get next batch of tracks
    results = sp.next(results) 

# TODO add filename to match the mood playlist
with open("FILE_NAME.json", 'w') as file:
        json.dump(tracks, file, indent=4)