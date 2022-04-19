import json
import logging
import pandas as pd
import spotipy as spot
from content_based import CBRecommend, normalize, ohe


CONFIG = json.load(
    open(file="song_recommender/config.json",
    encoding="utf-8"))
SCOPE = ["user-read-recently-played",
    "playlist-modify-public"]

def get_token(config:dict, username:str="frostcow") -> str:
    """Returns Spotify token string from config credentials. 
    Uses the Authorization flow.

    :param config (dict): Global config dict
    :param username (str): Username for token
    :return token (str): Spotify authorization token
    """
    return spot.util.prompt_for_user_token(
        username=username,
        scope=SCOPE,
        client_id=config["CLIENT_ID"],
        client_secret=config["CLIENT_SECRET"],
        redirect_uri=config["REDIRECT_URI"])

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

def get_last_50_songs(sp:spot.Spotify) -> pd.DataFrame:
    """Using the Spotify object, returns dataframe
    of the user's last 50 played songs.

    :param sp (spot.Spotify): Spotify client
    """
    response = sp.current_user_recently_played()
    all_tracks = [parse_track_info(item) for item in response['items']]
    # for item in response['items']:
    #     all_tracks.append(parse_track_info(item))
    headers = ['Track ID', 'Song Name',
        'Album Name', 'Artist Name', 'Explicit',
        'Duration', 'Song Popularity',
        'Album Release Date']
    tracks_df = pd.DataFrame(all_tracks, columns=headers)
    logging.info(" Formatted last 50 tracks in a DataFrame: \n%s",
        tracks_df.iloc[0])
    return tracks_df

def get_track_info(sp:spot.Spotify, tracks:list) -> list:
    print(tracks)
    response = sp.tracks(tracks)
    track_names = [track['name'] for track in response['tracks']]
    # track_info = [parse_track_info(item) for item in response['items']]
    # return track_info
    return track_names

def get_recommendation(df:pd.DataFrame, n_rec:int=5) -> pd.DataFrame:
    # normalize the num_pages, ratings, price columns
    df['duration_norm'] = normalize(df['Duration'].values)
    df['song_popularity'] = normalize(df['Song Popularity'].values)
    
    # OHE on publish_year and genre
    df = ohe(df = df, enc_col = 'Album Release Date')
    df = ohe(df = df, enc_col = 'Explicit')

    # drop redundant columns
    cols = ['Duration', 'Song Popularity', 'Album Release Date',
        'Song Name', 'Album Name', 'Artist Name', 'Explicit']
    df.drop(columns = cols, inplace = True)
    df.set_index('Track ID', inplace = True)
    
    # ran on a sample as an example
    t = df.copy()
    cbr = CBRecommend(df = t)
    return cbr.recommend(track_id=t.index[0], n_rec=n_rec)


def main():
    """Testing flow"""
    # Get token & Spotify client to get last 50 songs
    token = get_token(CONFIG)
    spotify = spot.Spotify(auth=token)
    last_50 = get_last_50_songs(spotify)
    recommended = get_recommendation(last_50)
    # Need to tear apart response track info
    print(get_track_info(spotify, recommended.index))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
