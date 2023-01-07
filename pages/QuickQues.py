import streamlit as st
from pages.Utilities.Utilities import Questions
from pathlib import Path


Questions.quick_questions(Path('pages\\Utilities\\questions\\quick_code_ques.py'))
st.write(st.session_state)
