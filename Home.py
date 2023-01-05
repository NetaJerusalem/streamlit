import pandas as pd
import streamlit as st
from pages.Utilities.Utilities import DataLoader, Utilities


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.title("Welcome to Neta Senionr Exercises")
st.write("Please select the required exercise on the left")
st.image("https://media.giphy.com/media/scZPhLqaVOM1qG4lT9/giphy.gif")


if Utilities.enter_name() == "admin":
    st.dataframe(DataLoader.df_names)
    if st.button("reload"):
        st.dataframe(DataLoader.load_df_status())
    DataLoader.download_status()
