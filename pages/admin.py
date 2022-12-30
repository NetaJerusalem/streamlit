

import pandas as pd
import streamlit as st
import os
import sys
from pages.Utilities.Utilities import DataLoader, Utilities


# status_df = pd.read_csv("pages\\data\\status.csv",skipinitialspace = True)
if Utilities.enter_name() == "admin":
    st.dataframe(DataLoader.df_names)
    if st.button("reload"):
        st.dataframe(DataLoader.load_df_status())
