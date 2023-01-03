import pandas as pd
import re
from typing import List, Tuple, Callable, TextIO, Final
import streamlit as st
from pathlib import Path
import subprocess
from streamlit_ace import st_ace
PASSWORD = "13245"


class DataLoader:
    # load data
    utilities_path = Path(__file__).parents[0]
    df_names = pd.read_csv(utilities_path / "names.csv", skipinitialspace=True)
    df_names["NAME"] = df_names["NAME"].map(str.strip)

    df_status = pd.read_csv(
        utilities_path / "status.csv", skipinitialspace=True)
    df_status["NAME"] = df_status["NAME"].map(str.strip)

    def load_df_names() -> pd.DataFrame:
        DataLoader.df_names = pd.read_csv(
            DataLoader.utilities_path / "names.csv", skipinitialspace=True)
        DataLoader.df_names["NAME"] = DataLoader.df_names["NAME"].map(
            str.strip)
        return DataLoader.df_names

    def load_df_status() -> pd.DataFrame:
        DataLoader.df_status = pd.read_csv(
            DataLoader.utilities_path / "status.csv", skipinitialspace=True)
        DataLoader.df_status["NAME"] = DataLoader.df_status["NAME"].map(
            str.strip)
        return DataLoader.df_status


class WriteAnswers:
    """
    Write the answer to csv file
    """

    def __init__(self, name: str, file_name: Path) -> None:
        assert name in DataLoader.df_names["NAME"].values or name == "admin", "Name must be in names"
        self.name = name
        self.file_name = file_name
        df_status = pd.read_csv(self.file_name, skipinitialspace=True)
        if self.name not in df_status["NAME"].values:
            df_status = pd.concat(
                [df_status, pd.DataFrame([{"NAME": self.name}])])
            df_status.to_csv(self.file_name, index=False)

    def add_answer(self,  answer: str, num_answers: int) -> None:
        """
        write answer to  csv file,
        Arg:
        answer:str - data to write to csv file
        num_answers:int - number of question to write
        """
        df = pd.read_csv(self.file_name, skipinitialspace=True, dtype="string")
        df.loc[df["NAME"] == self.name, str(num_answers)] = answer
        df.to_csv(self.file_name, index=False)


class Questions:
    def execute_question(num_questoin: int, questoin: str, test: Callable[[str], bool] = None,
                         write_answer: WriteAnswers = None, code: str = "", show_output: bool = True,
                         title: str = None, add_code: str = None, caption: str = None):
        # if title is not None
        form_title = title or f"Question {num_questoin}"
        with st.form(form_title):

            st.subheader(form_title)
            st.write(questoin)
            if caption:
                st.caption(caption)
            if add_code:
                code = add_code + code
            code = st_ace(value=code, language="python", auto_update=True).replace(code, '')

            # evaluate the code
            if st.form_submit_button("Submit") and code:
                output = subprocess.run(
                    ['python', '-c', code], capture_output=True, text=True).stdout
                if show_output:
                    st.code(output)
                if test and not test(output):
                    st.write("try again... code not match")
                write_answer.add_answer(code, num_questoin)

    def question(num_questoin: int, questoin: str, test: Callable[[str], bool] = None, write_answer: WriteAnswers = None, title: str = None):
        with st.form(f"Q {num_questoin}"):
            st.write(questoin)
            answer = st.text_input("Answer")
            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if test and not test(answer):
                st.write("try again... answer not match")
            elif submitted and answer:
                write_answer.add_answer(answer, num_questoin)

    def test_code_by_re(pattern: str) -> Callable[[str], bool]:
        def f(code: str) -> bool:
            f_pattern = re.compile(pattern)
            return bool(f_pattern.match(code))
        return f


class Utilities:
    """many tools"""
    def enter_name() -> str:
        """avoid load pange until user enter to system 
        and register the name in `st.session_state`

        Returns:
            str: name of user
        """
        if "user_name" not in st.session_state:
            # create a new placeholder for button and input fields
            plaseholder = st.empty()
            user_name: str = plaseholder.text_input(
                "Enter your username", autocomplete="name")
            # enter for admin
            if user_name == "admin":
                password_field = st.empty()
                password: str = password_field.text_input("Enter password")
                if password == PASSWORD:
                    st.session_state.user_name: str = user_name
                    plaseholder.success(
                        f'{user_name} Welcome to our system')
                    password_field.empty()
                    return user_name
            # entner for user
            elif user_name in DataLoader.df_names["NAME"].values:
                st.session_state.user_name: str = user_name
                plaseholder.success(f'{user_name} Welcome to our system')
                return user_name
            # if user not in names list
            elif user_name:
                st.write(
                    "your name not in names...\n enter your name like codebord name\n find your name in this list")
                st.dataframe(DataLoader.df_names["NAME"])

            st.stop()
        else:
            return st.session_state.user_name
