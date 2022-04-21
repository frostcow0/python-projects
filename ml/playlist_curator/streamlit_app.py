# Unfortunately there's an issue with the way Streamlit
# handles redirects & there's no way to use Spotify's
# API with it, as far as my research shows.
# Lots of people have run into this with no fix found yet.

import logging
import streamlit as st
import pandas as pd
from main import run_flow


logging.basicConfig(level=logging.INFO)

def get_recommendations() -> pd.DataFrame:
    """Calls run_flow and displays the recommended songs"""
    recommended = run_flow()
    st.markdown("## Songs added to your playlist!")
    st.table(recommended)

st.markdown("# Playlist Curator v0.5")
st.write(("An app that, using your recently played songs,"
    " creates a playlist of 20 songs tailored to you."
))

st.markdown("\n")
submit = st.button(label="Create my playlist!", on_click=get_recommendations)

st.markdown("\n")
st.write("Made by Jon Martin, last updated 4/20/22")
