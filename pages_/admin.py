import pandas as pd
import streamlit as st
# from pages.data.Utilities import df_names
import os




# status_df = pd.read_csv("pages\\data\\status.csv",skipinitialspace = True)
password = st.text_input("password")
if password == "13245":
    st.code(os.fspath("pages\\data\\status.csv"))
    # st.title("Welcome to Neta streamlit secend page")
    # # st.dataframe(df_names)
    # if st.button("relod"):
    #     # st.dataframe(status_df)




    
    