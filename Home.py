import pandas as pd
import streamlit as st
import os
# from pages.data.Utilities import WriteAnswer
from pathlib import Path

garret_burhenn_pitches_csv = Path(__file__).parents[1] / 'GarretBurhennData/Garret_Burhenn_Pitches.csv'
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.title("Welcome to Neta Senionr Exercises")

st.write("Please select the required exercise on the left")
st.image("https://media.giphy.com/media/scZPhLqaVOM1qG4lT9/giphy.gif")
st.code(os.fspath("pages_\\data\\status.csv"))
st.code(garret_burhenn_pitches_csv)
path = st.text_input("enter path")
buuton = st.button("load form path")
if buuton:
    st.dataframe(pd.read_csv(path))