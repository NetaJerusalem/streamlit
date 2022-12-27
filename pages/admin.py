import pandas as pd
import streamlit as st
names_df = pd.read_csv("data\\names.csv")
status_df = pd.read_csv("data\\status.csv")
password = st.text_input("password")
if password == "13245":
    st.title("Welcome to Neta streamlit secend page")
    st.dataframe(names_df)
    if st.button("relod"):
        st.dataframe(status_df)


    
    