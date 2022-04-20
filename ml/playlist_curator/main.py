import os
import logging
from typing import Tuple
from datetime import date
import pandas as pd
import spotipy as spot
from content_based import CBRecommend, normalize, ohe


# CONFIG = json.load(
#     open(file="config.json",
#     encoding="utf-8"))
SCOPE = ["user-read-recently-played",
    "playlist-modify-public",
    "user-library-read",]

def set_env_variables():
    """Manually sets environment variables"""
    os.environ["SPOTIPY_CLIENT_ID"] = "468b8b024bfb41d5b1957dad2afc766a"
    os.environ["SPOTIPY_CLIENT_SECRET"] = "8827668f8ed64f13bf8c2e83781c3997"
    os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8080"

def get_token() -> str:
    """Returns Spotify token string from config credentials.
    Uses the Authorization flow.

    :param config (dict): Global config dict
    :param username (str): Username for token
    :return token (str): Spotify authorization token
    """
    return spot.util.prompt_for_user_token(
        scope=SCOPE)

def parse_track_info(item) -> list:
    """Puts together a list of info from a response['item'].

    :param item (dict): Item from API response
    :return info (list): List of track info
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
    return [track_id, song_name, album_name,
        artist_name, explicit, duration,
        song_popularity, album_release_date]

def get_tracks_info(sp:spot.Spotify, tracks:list) -> pd.DataFrame:
    """Gets info for provided track IDs"""
    response = sp.tracks(tracks)
    tracks_info = [[track['name'], track['artists'][0]['name']] for track in response['tracks']]
    tracks_df = pd.DataFrame(tracks_info, columns=['Song Name', 'Artist Name'])
    tracks_df.index = [idx+1 for idx in tracks_df.index]
    return tracks_df

def get_last_50_songs(sp:spot.Spotify) -> pd.DataFrame:
    """Using the Spotify client, returns dataframe
    of the user's last 50 played songs.

    :param sp (spot.Spotify): Spotify client
    :return df (pd.DataFrame): 50 last played songs
    """
    response = sp.current_user_recently_played()
    all_tracks = [parse_track_info(item) for item in response['items']]
    headers = ['Track ID', 'Song Name',
        'Album Name', 'Artist Name', 'Explicit',
        'Duration', 'Song Popularity',
        'Album Release Date']
    tracks_df = pd.DataFrame(all_tracks, columns=headers)
    logging.info(" Formatted last 50 played tracks in a DataFrame: \n%s",
        tracks_df.iloc[0])
    return tracks_df

def get_saved_tracks(sp:spot.Spotify, limit:int=50) -> pd.DataFrame:
    """Using the Spotify client, returns dataframe
    of the user's last n saved tracks.

    :param sp (spot.Spotify): Spotify client
    :param limit (int): Number of songs to retrieve
    """
    headers = ['Track ID', 'Song Name',
        'Album Name', 'Artist Name', 'Explicit',
        'Duration', 'Song Popularity',
        'Album Release Date']
    tracks_df = pd.DataFrame(columns=headers)
    if limit > 50: # Spotify's request limit is 50
        counter = 0
        while limit > 0:
            if limit//50:
                limit -= 50
                n = 50
            else:
                n, limit = limit, 0
            response = sp.current_user_saved_tracks(limit=n, offset=counter*50)
            tracks = [parse_track_info(item) for item in response['items']]
            temp = pd.DataFrame(tracks, columns=headers)
            tracks_df:pd.DataFrame = pd.concat([tracks_df, temp], ignore_index=True)
            counter += 1
    else:
        response = sp.current_user_saved_tracks(limit=limit)
        tracks = [parse_track_info(item) for item in response['items']]
        temp = pd.DataFrame(tracks, columns=headers)
        tracks_df:pd.DataFrame = pd.concat([tracks_df, temp], ignore_index=True)
    logging.info(" Formatted %s most recent saved tracks in a DataFrame: \n%s",
        tracks_df.shape[0], tracks_df.iloc[0])
    return tracks_df

def prep_dataframes(saved:pd.DataFrame, last:pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Helper function for get_recommendation"""
    df_s = saved.copy()
    df_l = last.copy()

    # normalize the num_pages, ratings, price columns
    df_s['duration_norm'] = normalize(df_s['Duration'].values)
    df_s['song_popularity'] = normalize(df_s['Song Popularity'].values)
    df_l['duration_norm'] = normalize(df_l['Duration'].values)
    df_l['song_popularity'] = normalize(df_l['Song Popularity'].values)

    # OHE on Album Release Date and Explicit - have to be done together
    df_s, df_l = ohe(saved=df_s, last=df_l)

    # drop redundant columns
    cols = ['Duration', 'Song Popularity',
        'Song Name', 'Album Name', 'Artist Name']
    df_s.drop(columns = cols, inplace = True)
    df_s.set_index('Track ID', inplace = True)
    df_l.drop(columns = cols, inplace = True)
    df_l.set_index('Track ID', inplace = True)
    logging.info(" Prepped saved & last played songs")
    return df_s, df_l

def get_recommendation(saved:pd.DataFrame, last:pd.DataFrame, n_rec:int=5) -> pd.DataFrame:
    """Uses cosine similarity to get recommended songs from the user's saved songs"""
    prepped_saved, prepped_last = prep_dataframes(saved, last)
    cbr = CBRecommend(df=prepped_saved)
    prepped_last.reset_index(drop=True, inplace=True)
    averaged_vector = prepped_last.mean(axis=0)
    return cbr.recommend(inputVec=averaged_vector, n_rec=n_rec)

def create_playlist(sp:spot.Spotify, user_id:str) -> str:
    """Creates playlist for the user"""
    today = date.today().strftime("%m/%d/%Y")
    playlist_name = f"{today} Playlist"
    playlist_description = ("This playlist was made by Jon's Playlist Curator"
        f" on {today}. I hope you like it!")
    sp.user_playlist_create(user=user_id,
        name=playlist_name, description=playlist_description)
    logging.info(" Created the playlist for the user")
    return playlist_name

def add_playlist_songs(sp:spot.Spotify, recommended:pd.DataFrame, user_id:str) -> None:
    """Adds songs to user's most recently made playlist"""
    created_playlist = sp.user_playlists(user=user_id, limit=1)
    playlist_id = created_playlist['items'][0]['id']
    sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id,
        tracks=recommended.index)
    logging.info(" Added the recommended tracks to the playlist")

def run_flow():
    """Testing flow"""
    # Get token & Spotify client to get last 50 songs
    set_env_variables() # for running locally
    logging.info(" Requesting token")
    token = get_token()
    logging.info(" Creating Spotify client")
    spotify = spot.Spotify(auth=token)
    logging.info(" Getting current user ID")
    user_id = spotify.current_user()['id']
    logging.info(" Getting saved tracks")
    saved = get_saved_tracks(spotify, limit=2000)
    logging.info(" Getting recently played songs")
    last_50 = get_last_50_songs(spotify)
    logging.info(" Getting recommendations")
    recommended = get_recommendation(saved, last_50, n_rec=20)
    logging.info(" Formatting recommendations")
    nice_format_recommend = get_tracks_info(spotify, recommended.index)
    logging.info(" The recommended songs are: \n%s",
        nice_format_recommend)

    # create_playlist(spotify, user_id)
    # add_playlist_songs(spotify, recommended, user_id)

    return nice_format_recommend

    # Future additions:
    #   add genre to the songs (from artist)
    #   add audio features per song (heavy compute cost, big benefit)
    #   store saved songs to add collaborative filtering/hybrid algorithm
    #   edit playlist songs if they've already used this to make a playlist today


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_flow()
