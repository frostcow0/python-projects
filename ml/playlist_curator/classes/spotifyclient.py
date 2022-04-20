import json
import requests

from classes.track import Track
from classes.playlist import Playlist


class SpotifyClient:
    """SpotifyClient performs operations using the Spotify API"""

    def __init__(self, authorization_token, user_id):
        """
        :param authorization_token (str): Spotify API token
        :param user_id (int): Spotify user id
        """
        self.authorization_token = authorization_token
        self.user_id = user_id

    def get_last_played_tracks(self, limit=10):
        """Get the last n tracks played by a user

        :param limit (int): Number of tracks to get. Should be <=50
        :return tracks (list of Track): List of last played tracks
        """
        url = f"https://api.spotify.com/v1/me/player/recently-played?limit={limit}"
        response = self._place_get_api_request(url)
        response_json = response.json()
        tracks = []
        for track in response_json['items']:
            name = track['track']['name']
            id = track['track']['id']
            artist = track['artists'][0]['name']
            tracks.append(Track(name, id, artist))
        return tracks

    def get_track_recommendations(self, seed_tracks, limit=50):
        """"""
        # To be implemented personally
        pass

    def _place_get_api_request(self, url):
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.authorization_token}"
            }
        )
        return response
