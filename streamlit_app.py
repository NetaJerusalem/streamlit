from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from Utilities import WriteData

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
    st.button("playground")
    