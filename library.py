import json

import spotipy
from spotipy.oauth2 import SpotifyOAuth

#TODO
# go into developers.spotify.com and use the client ID and secret like you did in HW1
# make sure the REDIRECT_URI is the same as the one specified here!!!!
CLIENT_ID = '5136eebddeac4d10b82bb55a64dcf00e'
CLIENT_SECRET = 'a165c457e8e34acd97afa9e2cb812234'
REDIRECT_URI = 'http://localhost:8888/callback'

# Define the scopes you need
SCOPE = 'user-library-read'

# Create a SpotifyOAuth object
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
)

# Get the authorization URL
auth_url = sp_oauth.get_authorize_url()
print("Please visit this URL for authorization:", auth_url)

# Get the authorization code from the user
#TODO
# after clicking the link, you will get redirected to a localhost:8888/callback?code={random chars}
# copy the code and paste it into the console. It will take a second and then all of your songs will be added to
# a json file :)
auth_code = input("Enter the authorization code: ")

# Get the access token
token_info = sp_oauth.get_access_token(auth_code)

# Create a Spotipy object with the access token
sp = spotipy.Spotify(auth=token_info['access_token'])

# Get the user's liked songs
results = sp.current_user_saved_tracks()
liked_songs = []

while results:
    for item in results['items']:
        track = item['track']
        liked_songs.append({
            'name': track['name'],
            'uri': track['uri']
        })

    if results['next']:
        results = sp.next(results)
    else:
        results = None

#TODO rename the file so that it does not overwrite anyone else's
with open('liked_songs_1.json', 'w') as json_file:
    json.dump(liked_songs, json_file, indent=4)
