import logging
import pandas as pd
import streamlit as st
from streamlit import session_state as ses
from __init__ import DataLoader, Utilities, Writer


st.session_state.names = DataLoader("names_and_answers/names.csv")

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.title("Welcome to Neta Senionr Exercises")
st.markdown("Please select the required exercise on the left `code` text")
st.image("https://media.giphy.com/media/scZPhLqaVOM1qG4lT9/giphy.gif")
writer = Writer("test_ai", "Sheet1")

if Utilities.enter_name(st.session_state.names) == "admin":
    logging.info("admin entering")

    status_ex1: DataLoader = DataLoader("names_and_answers/answers_ex1.csv")
    status_multi: DataLoader = DataLoader("names_and_answers/answers_multi.csv")
    st.write("### ex1 ")
    placeHolder_ex1 = st.empty()
    st.write("### multi ")
    if st.button("reload"):
        status_multi.reload()
        status_ex1.reload()
    status_ex1.download()
    status_multi.download()


def __write_to_file():
    writer.write(ses.col, ses.row, ses.data)


st.number_input("column", key="col")
st.number_input("row", key="row")
st.text_input("data", key="data", on_change=__write_to_file)
