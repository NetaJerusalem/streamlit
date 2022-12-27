import pandas as pd
import streamlit as st
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from Utilities import AddAnswer

st.set_page_config(page_title="Ex1", page_icon="📈")

with open("data\\sattus.csv", "w") as f:
    write = AddAnswer(f)
    
st.title("Welcome to Neta streamlit secend page")

with st.form("Q 1"):
   st.write("Qua")
   name = st.text_input("Form checkbox")
   answer = st.text_input("Answer")

   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
        df = df.append({"name": name}, ignore_index=True)
        df.to_csv("names.csv", index=False)
