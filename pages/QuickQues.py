import streamlit as st
from pages.Utilities.Utilities import Questions
from pathlib import Path


Questions.quick_questions("quick_code_ques.py")
st.write(st.session_state)
