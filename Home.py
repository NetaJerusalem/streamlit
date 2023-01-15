from logging import PlaceHolder
import pandas as pd
import streamlit as st
from streamlit import session_state as ses
from pages.Utilities.Utilities import DataLoader, Utilities


st.session_state.names = DataLoader("names.csv")

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.title("Welcome to Neta Senionr Exercises")
st.write("Please select the required exercise on the left")
st.image("https://media.giphy.com/media/scZPhLqaVOM1qG4lT9/giphy.gif")


if Utilities.enter_name(st.session_state.names) == "admin":
    status_ex1: DataLoader = DataLoader("answers_ex1.csv")
    status_multi: DataLoader = DataLoader("answers_multi.csv")
    st.write("### ex1 ")
    placeHolder_ex1 = st.empty()
    st.write("### multi ")
    placeHolder_multi = st.empty()
    placeHolder_ex1.dataframe(status_ex1.df)
    placeHolder_multi.dataframe(status_multi.df)
    if st.button("reload"):
        status_multi.reload()
        status_ex1.reload()
    status_ex1.download()
    status_multi.download()

    st.write(ses)