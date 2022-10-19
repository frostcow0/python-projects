# Unfortunately there's an issue with the way Streamlit
# handles redirects & there's no way to use Spotify's
# API with it, as far as my research shows.
# Lots of people have run into this with no fix found yet.

import logging
import streamlit as st
from main import get_recommendations, get_user_data, save_playlist


logging.basicConfig(level=logging.INFO)

@st.cache(allow_output_mutation=True)
def fetch_user_data() -> dict:
    """Pulls user's saved and recently played songs"""
    return get_user_data()

def run_recommender(data:dict, method:str="cosine") -> None:
    """Calls get_recommendations and displays the recommended songs"""
    formatted, raw = get_recommendations(data, method)
    st.markdown(f"## Recommended songs using {method.title()} distance below!")
    st.write("Click the \"Save this Playlist\" button below"
        " to save these songs.")
    st.table(formatted)
    st.button(label="Save this playlist",
        on_click=lambda:save_playlist(raw))

# Run this and cache the data, means that users can go back and forth
# between the distance measures without any hassle
user_data = fetch_user_data()

st.markdown("# Playlist Curator v0.7")
st.write(("An app that, using your recently played songs,"
    " creates a playlist of 20 songs tailored to you."
))

st.markdown("\n")
st.button(label="Use Cosine Distance",
    on_click=lambda : run_recommender(user_data, method="cosine"))
st.button(label="Use Minkowski Distance",
    on_click=lambda : run_recommender(user_data, method="minkowski"))

st.markdown("\n")
st.write("Made by Jon Martin, last updated 10/11/22")
