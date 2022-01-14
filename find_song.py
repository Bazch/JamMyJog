import random
import pandas as pd
import numpy as np
import add_song_to_playlist as playlist

genres = ['hip hop', 'r&b']
pd.set_option('display.max_columns', 10)
df = pd.read_csv('./resources/music.csv')

df_format = df[['artist.name', 'title', 'tempo', 'terms', 'artist.id', 'similar']]



def find_song_to_bpm(bpm, genre_list):
    subset = df_format.loc[(df_format['terms'].isin(genres)) & (df_format['tempo'] <= bpm + 5) & (df_format['tempo'] >= bpm - 5)]
    dc = subset.to_dict('list')
    artists = dc.get("artist.name")
    songs = dc.get("title")
    combined = np.array((artists, songs)).T
    random_pick = random.choice(combined)
    return random_pick[0],random_pick[1]


def final_final_final(bpm, genre_list=genres):
    artist, song = find_song_to_bpm(bpm, genres)
    if artist is not None or song is not None:
        playlist.find_track_and_add_to_playlist(artist, song)
