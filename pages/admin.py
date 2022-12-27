import pandas as pd
import streamlit as st
names = pd.read_csv("data\\names.csv")
password = st.text_input("password")
if password == "13245":
    st.title("Welcome to Neta streamlit secend page")
    st.dataframe(names)

    st.subheader("playground")
    with st.echo(code_location='below'):
        st.button("playground")
    
    