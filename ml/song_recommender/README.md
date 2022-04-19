# Song Recommender
A project utilizing Spotify's API and the matching Python library spotipy to create personalized 20-song playlists based on the current user's recent listening history.

## The Process
1. Getting data from an API (Spotify)
2. Data wrangling
3. Prototype model
4. Solidify flow for steps 1-3
5. Deploy using Flask
6. Refactor / Best practices
7. Future plans

## Getting data from an API
It took several reads through [spotipy's docs](https://spotipy.readthedocs.io/en/2.19.0/) to understand the usage of scope and credentials. Once I established a working "client" I was able to test run some API calls in a Jupyter Notebook. The coolest call I encountered was `sp.audio_features` for sure. It returns a variety of Spotify metrics from danceability to liveliness and energy. Thanks to the spotipy Python library this step was relatively short, but it also made me realize that I need to take the time separately to practice making my own API calls.


## Data wrangling
In the same aforementioned Jupyter Notebook I practiced a variety of pandas methods for reshaping the data, reshaping it again, reshaping it some more. My favorite method that I've recently picked up is `pd.pivot_table`, turns out they're not just for Excel!

## Prototype model
