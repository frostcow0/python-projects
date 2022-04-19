import json
import logging
import pandas as pd
import spotipy as spot
from content_based import CBRecommend, normalize, ohe


CONFIG = json.load(
    open(file="song_recommender/config.json",
    encoding="utf-8"))
SCOPE = ["user-read-recently-played",
    "playlist-modify-public",
    "user-library-read",]

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

def get_tracks_info(sp:spot.Spotify, tracks:list) -> pd.DataFrame:
    print(tracks)
    response = sp.tracks(tracks)
    tracks_info = [[track['name'], track['artists'][0]['name']] for track in response['tracks']]
    tracks_df = pd.DataFrame(tracks_info, columns=['Song Name', 'Artist Name'])
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

def clean_dataframe(input:pd.DataFrame) -> pd.DataFrame:
    """Helper function for get_recommendation"""
    df = input.copy()

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
    return df

def get_recommendation(saved:pd.DataFrame, last:pd.DataFrame, n_rec:int=5) -> pd.DataFrame:
    cleaned_saved = clean_dataframe(saved)
    cleaned_last = clean_dataframe(saved)

    # ran on a sample as an example
    t = cleaned_saved.copy()
    cbr = CBRecommend(df = t)
    cleaned_last.reset_index(drop=True, inplace=True)
    averaged_vector = cleaned_last.mean(axis=0)
    return cbr.recommend(inputVec=averaged_vector, n_rec=n_rec)

def main():
    """Testing flow"""
    # Get token & Spotify client to get last 50 songs
    token = get_token(CONFIG)
    spotify = spot.Spotify(auth=token)
    saved = get_saved_tracks(spotify, limit=2000)
    last_50 = get_last_50_songs(spotify)
    recommended = get_recommendation(saved, last_50)
    print(get_tracks_info(spotify, recommended.index))
    # Need to supply all liked songs, or at least a few hundred
    # for better results

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
