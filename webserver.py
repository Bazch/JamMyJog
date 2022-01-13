from __future__ import print_function
from http.server import HTTPServer, BaseHTTPRequestHandler
import spotipy
from spotipy import oauth2
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIPY_CLIENT_ID = 'dc57f4d2e2f144bda26caaeabb73fa00'
SPOTIPY_CLIENT_SECRET = '88e3cc5852b6428388cce8340b77a800'
PORT = 8080
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'
authUrl = "https://accounts.spotify.com/api/token"
sp_credentials = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )
sp = spotipy.Spotify(client_credentials_manager=sp_credentials, auth_manager=sp_credentials)

song = sp.search(q='artist: Linkin Park track: Numb')


class helloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        str = "<a href='" + sp_oauth.get_authorize_url() + "'>Login to Spotify</a>"
        self.wfile.write(str.encode())

def main():
    server = HTTPServer(('', PORT), helloHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()

if __name__ == '__main__':
    main()