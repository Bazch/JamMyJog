import flask
from flask import Flask, render_template, request

import spotipy
from spotipy import oauth2
from spotipy.oauth2 import SpotifyClientCredentials
import find_song

SPOTIPY_CLIENT_ID = 'dc57f4d2e2f144bda26caaeabb73fa00'
SPOTIPY_CLIENT_SECRET = '88e3cc5852b6428388cce8340b77a800'
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'
authUrl = "https://accounts.spotify.com/api/token"
sp_credentials = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)

sp = spotipy.Spotify(client_credentials_manager=sp_credentials, auth_manager=sp_credentials)

app = Flask(__name__)

@app.route('/')
def hello():
    SPOTIPY_REDIRECT_URI = request.base_url + 'slider'
    sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE, cache_path=CACHE, open_browser=True)
    url = sp_oauth.get_authorize_url()
    print(url)
    return render_template("index.html", spotifyAuthLink=sp_oauth.get_authorize_url())
@app.route('/slider', methods=['GET', 'POST'])
def slider():
    if request.method == 'GET':
        return render_template("slider.html")
    elif request.method == 'POST':
        bpm = int(request.values.get('value'))
        print(bpm)
        find_song.final_final_final(bpm, ['progressive house'], 5)
        return render_template("slider.html")
if __name__ == "__main__":
    app.run(debug=True)