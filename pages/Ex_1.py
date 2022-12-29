import streamlit as st
import pandas as pd
from pages.Utilities.Utilities import WriteAnswer, Utility, Questions
df_status = Utility.df_status
df_names = Utility.df_names
utilities_path = Utility.utilities_path


st.set_page_config(page_title="Ex1", page_icon="📈")
name = st.text_input("Enter your name")
if name and name not in df_names["NAME"].values:
    st.write("your name not in names...\n enter your name like codebord name\n find your name in this list")
    st.dataframe(df_names)
    st.stop()
elif name:
    write_answer = WriteAnswer(name, utilities_path / "status.csv")
    st.title(f"{name} Welcome to Neta Ex 1")
    df_status = Utility.load_df_status()
    st.dataframe(df_status.loc[df_status["NAME"] ==
                 name], use_container_width=True)

    Questions.execute_question(1, '''Printing the numbers 1 through 10: 
     _remember_ `range(x,y)` run from x to y-1''',
                               write_answer=write_answer
                               )

    Questions.execute_question(2, "Printing the elements of a list of strings:",
                               code='my_list = ["apple", "banana", "cherry"]',
                               write_answer=write_answer
                               )

    Questions.execute_question(3, "Printing the to the power of 2 every number of a list of numbers:",
                               code='my_list = [1, 2, 3, 4, 5]',
                               write_answer=write_answer
                               )

    Questions.execute_question(4, "Printing the elements of my_list[0]:",
                               code='my_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]',
                               write_answer=write_answer
                               )
    Questions.execute_question(5, "Printing the elements of a list of lists:",
                               code='my_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]',
                               write_answer=write_answer
                               )
    Questions.execute_question(6, "Printing the elements of a string one character at a time",
                               code='my_string = "Hello, world!"',
                               write_answer=write_answer)
    Questions.execute_question(7, '''Printing the numbers 0 through 29,
                                         but only the ones that are multiples of 3: _using `range()`_''',
                               write_answer=write_answer)
    Questions.execute_question(8, '''Printing the elements of a list of numbers,
                                        but only the ones that are divisible by both 2 and 3:''',
                               code='my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13]',
                               write_answer=write_answer)
