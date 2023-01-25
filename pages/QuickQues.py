import streamlit as st
from pages.Utilities.Utilities import Questions, Utilities, QuickQuestions
from pathlib import Path

st.set_page_config(page_title="Quick Questions", page_icon="🔢",initial_sidebar_state="collapsed")
QuickQuestions("quick_ques_function.py",seconds=3, num_questoin=1)

