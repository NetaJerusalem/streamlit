import streamlit as st
from pages.Utilities.Utilities import Questions
from pathlib import Path
st.set_page_config(page_title="Multiplication table",
                   page_icon="🔢")

Questions.quick_questions("quick_code_ques.py")
