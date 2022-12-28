import pandas as pd
import streamlit as st
import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from pages.Utilities.Utilities import Utility



# status_df = pd.read_csv("pages\\data\\status.csv",skipinitialspace = True)
password = st.text_input("password")
if password == "13245":
    st.title("admin")
    st.dataframe(Utility.df_names)
    if st.button("relod"):
        st.dataframe(Utility.df_status)




    
    