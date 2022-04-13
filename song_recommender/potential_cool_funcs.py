import json
import spotipy as sp
import pandas as pd
import logging


CONFIG = json.load(open(file="song_recommender/config.json", encoding="utf-8"))
SCOPE = "user-read-recently-played"

def get_auth(config:dict) -> sp.SpotifyOAuth:
    """Returns SpotifyOAuth object from config credentials"""
    return sp.SpotifyOAuth(
        client_id=config["CLIENT_ID"],
        client_secret=config["CLIENT_SECRET"],
        redirect_uri=config["REDIRECT_URI"],
        scope=SCOPE,
    )

def get_info(item) -> list:
    """
    Puts together a list of info from a results['item'].
    
    Returns: 
        [track_id, song_name, album_name, artist_name,
    explicit, duration, song_popularity, album_release_date]
    """
    track = item['track']
    track_id = track['id']
    song_name = track['name']
    album_name = track['album']['name']
    artist_name = track['artists'][0]['name']
    explicit = track['explicit']
    duration = track['duration_ms']
    song_popularity = track['popularity']
    album_release_date = track['album']['release_date']
    return [track_id, song_name, album_name, artist_name, explicit,
        duration, song_popularity, album_release_date]

def get_audio_features(sp:sp.Spotify, track_ids:list) -> pd.Series:
    """Uses's Spotify's audio_features api call to build a Series of
    tracks and their features"""
    result = sp.audio_features(track_ids)
    return pd.DataFrame.from_dict(result)

def get_last_50_songs(sp:sp.Spotify) -> pd.DataFrame:
    """Using the Spotify object, returns dataframe of the user's
    last 50 played songs"""
    results = sp.current_user_recently_played()
    all_tracks = []
    for item in results['items']:
        all_tracks.append(get_info(item))
    headers = ['Track ID', 'Song Name', 'Album Name', 'Artist Name',
        'Explicit', 'Duration', 'Song Popularity', 'Album Release Date']
    tracks_df = pd.DataFrame(all_tracks, columns=headers)
    logging.info(" Formatted last 50 tracks in a DataFrame: \n%s",
        tracks_df.loc[0])
    return tracks_df

def main():
    """Testing flow"""
    # Create auth & Spotify client to get last 50 songs
    # and the audio features for each of the songs
    auth = get_auth(CONFIG)
    spotify = sp.Spotify(auth_manager=auth)
    last_50 = get_last_50_songs(spotify)
    audio_features = get_audio_features(
        spotify, last_50['Track ID'].to_list())
    # Merge the last 50 songs and their respective
    # audio features, then sort on danceability
    # and dropping duplicates 
    # (yes I often listen to the same song)
    merged_df = pd.merge(last_50, audio_features,
        left_on='Track ID', right_on='id')
    reduced_df = merged_df.loc[:, # Better to use loc (row, column)
        ('Song Name', 'Album Name', 'danceability')]
    reduced_df.sort_values(by='danceability',
        ascending=False, inplace=True)
    reduced_df.drop_duplicates(inplace=True)

    print(reduced_df.head())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
