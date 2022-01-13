import base64, json
import requests

CLIENT_ID = 'dc57f4d2e2f144bda26caaeabb73fa00'
CLIENT_SECRET = '88e3cc5852b6428388cce8340b77a800'
SCOPES = 'playlist-modify-public'
authUrl = "https://accounts.spotify.com/api/token"

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

    print(json.dumps(track_object, indent=2))
    return song_ID


token = getAccessToken(CLIENT_ID, CLIENT_SECRET)
artist = "Linkin Park"
title = "Numb"

track = getTrack(token, artist, title)

print(token)

print(track)
