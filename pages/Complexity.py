import sys
import os
import streamlit as st
import pandas as pd
import numpy as np
from streamlit import session_state as ses
from __init__ import WriteAnswers, Questions, Utilities, DataLoader

names_df: DataLoader = DataLoader("names_and_answers/names.csv")
status_df: DataLoader = DataLoader("names_and_answers/answers_ex1.csv")

st.set_page_config(
    page_title="Complexity", page_icon="🔢", initial_sidebar_state="collapsed"
)

name = Utilities.enter_name(names_df)
write_answers: WriteAnswers = WriteAnswers(name, status_df)
st.title(f"{name} Welcome to Ex1")
st.dataframe(
    status_df.df.loc[status_df.df["NAME"] == name].replace([np.nan, " "], "🤔"),
    use_container_width=True,
)
st.write(ses)
Questions.regular_question(
    "q1",
    1,
    """
    Create a function that takes a number as an input and __returns__ the square of that number
    """,
    "n",
    code="""import time\n\ndef f1(n):\n\tfor i in range(n):\n\t\tdo_something()""",
    write_answer=write_answers,
    code_add_before="import time\ndo_something = lambda : time.sleep(0.001)",
)

Questions.regular_question(
    "q2",
    2,
    """
    Create a function that takes a number as an input and __returns__ the square of that number
    """,
    "n",
    code="""import time\n\ndef f1(n):\n\tfor i in range(n):\n\t\tdo_something()""",
    write_answer=write_answers,
    code_add_before="import time\ndo_something = lambda : time.sleep(0.001)",
)
Questions.regular_question(
    "q3",
    3,
    """
    Create a function that takes a number as an input and __returns__ the square of that number
    """,
    "n**2",
    write_answer=write_answers,
)
