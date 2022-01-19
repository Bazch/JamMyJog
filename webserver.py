from __future__ import print_function
from http.server import HTTPServer, BaseHTTPRequestHandler
import spotipy
from flask import Flask
from spotipy import oauth2
from spotipy.oauth2 import SpotifyClientCredentials
import find_song

import flask



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
hostName = "localhost"
serverPort = 8080

song = sp.search(q='artist: Linkin Park track: Numb')
genres = ['progressive house']



class helloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path == "/slider":
            print(self.path)
            self.display_slider()
            return
        elif self.path == "/":
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            str = "<a href='" + sp_oauth.get_authorize_url() + "'>Login to Spotify</a></br>"
            str += "<input type=\"button\" onclick=\"goToSlider()\" value=\"Navigate to slider\"></input>"
            self.wfile.write(str.encode())
        elif self.path == "/static/front.js":
            self.send_response(200)
            self.send_header('Content-type', 'text/javascript')
            self.end_headers()
            f = open("static/front.js", "rb")
            for each_line in f:
                self.wfile.write(each_line)
            return
        else:
            self._set_response()

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()


    def display_slider(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        output = ''
        output += "<html><head><title>Barry's Hi-Fi prototype</title>"
        output += "<script type=\"text/javascript\" charset=\"utf8\" src=\"static/front.js\"></script></head>"
        output += "<p>Request: %s</p>" % self.path
        output += "<body>"
        output += "<p><span id=\"textSliderValue\">%SLIDERVALUE%</span></p>"
        output += "<p><input type=\"range\" onchange=\"updateSliderPWM(this)\" id=\"pwmSlider\" min=\"0\" max=\"255\" value=\"%SLIDERVALUE%\" step=\"1\" class=\"slider\"></p>"
        output += "<p>Slide to adjust BPM</p>"
        output += "</body><html>"
        self.wfile.write(output.encode("utf-8"))

    def do_POST(self):
        self._set_response()
        content_length = int(self.headers['Content-Length'])
        bpm = int(self.rfile.read(content_length).decode("utf-8"))
        find_song.final_final_final(bpm, genres, 5)


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), helloHandler)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")