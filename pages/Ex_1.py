from Utilities import WriteAnswer
import pandas as pd
import streamlit as st
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
names = pd.read_csv("data/names.csv")

st.set_page_config(page_title="Ex1", page_icon="📈")
name = st.text_input("enter your name")
if name and name not in names["NAME"].values:
    st.write("your name not in names...\n enter your name like codebord name\n find your name in this list")
    st.dataframe(names)
    st.stop()
elif name:
    write_answer = WriteAnswer(name, "data/status.csv")
    st.title("Welcome to Neta Ex 1")
    df_status = pd.read_csv("data/status.csv")
    st.dataframe(df_status.loc[df_status["NAME"]== name])

    with st.form("Q 1"):
        st.write("Qua")
        answer = st.text_input("Answer")
    # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            write_answer.add_answer(answer, 1)



    with st.form("Q 2"):
        st.code("""for i in range(10):
                        for j in range(10):
                            print (i*j)""")
        answer = st.text_input("Answer")

    # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            write_answer.add_answer(answer, 2)



    with st.form("Q 3"):
        st.write("Qua")
        answer = st.text_input("Answer")

    # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            write_answer.add_answer(answer, 3)


    with st.form("Q 4"):
        st.write("Qua")
        answer = st.text_input("Answer")
    # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            write_answer.add_answer(answer, 4)
