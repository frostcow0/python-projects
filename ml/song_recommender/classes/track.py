class Track:
    """Track is a piece of music on Spotify"""

    def __init__(self, name, id, artist):
        """
        :param name (str): Track name
        :param id (int): Spotify teack id
        :param artist (str): Artist of the track
        """
        self.name = name
        self.id = id
        self.artist = artist

    def create_spotify_uri(self):
        """Returns track ID formatted as Spotify uri"""
        return f"spotify:track:{self.id}"

    def __str__(self):
        return f"{self.name} by {self.artist}"
