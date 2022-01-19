import base64, json
import time

import requests
import spotipy
from spotipy import oauth2

CLIENT_ID = 'dc57f4d2e2f144bda26caaeabb73fa00'
CLIENT_SECRET = '88e3cc5852b6428388cce8340b77a800'
SCOPE = 'user-library-read playlist-modify-private playlist-read-collaborative playlist-read-private playlist-modify-public user-library-modify user-library-read app-remote-control user-read-playback-position user-top-read user-read-recently-played user-read-playback-state user-modify-playback-state user-read-currently-playing'
REDIRECT_URI = 'http://127.0.0.1:5000/slider/'
authUrl = "https://accounts.spotify.com/api/token"
PLAYLIST_ID = '14CyMjWKnsnOulk6t8DqTy'
CACHE = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE,
                               open_browser=True, cache_path=CACHE)
sp = spotipy.client.Spotify(oauth_manager=sp_oauth)

authHeader = {}
authData = {}


def getAccessToken(clientID, client_secret):
    message = f"{clientID}:{client_secret}"
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    authHeader['Authorization'] = "Basic " + base64_message
    authData['grant_type'] = "client_credentials"

    res = requests.post(authUrl, headers=authHeader, data=authData)

    response_object = res.json()

    access_token = response_object['access_token']

    return access_token


def getTrack(token, artist, title):
    search_endpoint = f"https://api.spotify.com/v1/search?type=track&q=artist:{artist}+track:{title}"
    get_header = {"Authorization": "Bearer " + token}
    res = requests.get(search_endpoint, headers=get_header)
    track_object = res.json()
    song_ID = track_object['tracks']['items'][0]['id']

    return song_ID


def add_to_playlist(playlist_id, tracks):
    sp.playlist_add_items(playlist_id=playlist_id, items=tracks)


def find_track_and_add_to_playlist(artist, title):
    token = getAccessToken(CLIENT_ID, CLIENT_SECRET)
    tracks = [getTrack(token, artist, title)]
    add_to_playlist(PLAYLIST_ID, tracks)
    time.sleep(1)
    sp.next_track()



