import pandas as pd
import streamlit as st
from pages.Utilities.Utilities import DataLoader, Utilities


if Utilities.enter_name() == "admin":
    st.dataframe(DataLoader.df_names)
    if st.button("reload"):
        st.dataframe(DataLoader.load_df_status())
