import streamlit as st
from __init__ import Questions, Utilities, QuickQuestions ,QuickQuestionsNoBar
from pathlib import Path

st.set_page_config(page_title="Quick Questions", page_icon="🔢",initial_sidebar_state="collapsed")
QuickQuestionsNoBar("cods_questions/slicing.py", num_questoin=1)

