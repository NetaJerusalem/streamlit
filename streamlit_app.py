from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from Utilities import WriteData

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""
st.title("Welcome to Neta streamlit project")

import streamlit as st
import pandas as pd
df = pd.read_csv("names.csv")

# Write the name to the CSV file

with st.form("enter name"):
   st.write("Inside the form")
   name = st.text_input("Form checkbox")

   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
        df = df.append({"name": name}, ignore_index=True)
        df.to_csv("names.csv", index=False)

st.write("Outside the form")

# Every form must have a submit button.
external_name = st.text_input("external name")
if external_name:
    df = df.append({"name": external_name}, ignore_index=True)
    df.to_csv("names.csv", index=False)

st.dataframe(df)
st.subheader("playground")
with st.echo(code_location='below'):
    pass
    