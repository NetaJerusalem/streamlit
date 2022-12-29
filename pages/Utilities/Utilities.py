import pandas as pd
import re
from typing import List, Tuple, Callable, TextIO
import streamlit as st
from pathlib import Path
import subprocess
from streamlit_ace import st_ace


class Utility:
    # load data
    utilities_path = Path(__file__).parents[0]

    df_names = pd.read_csv(utilities_path / "names.csv", skipinitialspace=True)
    df_names["NAME"] = df_names["NAME"].map(str.strip)

    df_status = pd.read_csv(
        utilities_path / "status.csv", skipinitialspace=True)
    df_status["NAME"] = df_status["NAME"].map(str.strip)

    def load_df_names() -> pd.DataFrame:
        Utility.df_names = pd.read_csv(
            Utility.utilities_path / "names.csv", skipinitialspace=True)
        Utility.df_names["NAME"] = Utility.df_names["NAME"].map(str.strip)
        return Utility.df_names

    def load_df_status() -> pd.DataFrame:
        Utility.df_status = pd.read_csv(
            Utility.utilities_path / "status.csv", skipinitialspace=True)
        Utility.df_status["NAME"] = Utility.df_status["NAME"].map(str.strip)
        return Utility.df_status


class WriteAnswer:
    """
    Write the answer to csv file
    """

    def __init__(self, name: str, file_name: Path) -> None:
        assert name in Utility.df_names["NAME"].values, "Name must be in names"
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
        st.write("good job!")


class Questions:
    def execute_question(num_questoin: int, questoin: str, test: Callable[[str], bool] = None,
                         write_answer: WriteAnswer = None, code: str = None, show_output: bool = True,
                         title: str = None, add_code: str = None):
        # if title is not None
        form_title = title or f"Question {num_questoin}"
        with st.form(form_title):
            st.write(questoin)
            code = st_ace(value=code, language="python", auto_update=True)

            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            st.caption(''' Please note: :sunglasses:   \
            you can only see what is printed in the form through the `print` command,
            you cannot see errors, or commands that are not printed''')

            # evaluate the code
            if add_code:
                code = add_code + code
            output = subprocess.run(
                ['python', '-c', code], capture_output=True, text=True).stdout
            if show_output:
                st.code(output)
            if test and not test(output):
                st.write("try again... code not match")
            elif submitted and code:
                write_answer.add_answer(code, num_questoin)

    def question(num_questoin: int, questoin: str, test: Callable[[str], bool] = None, write_answer: WriteAnswer = None, title: str = None):
        with st.form(f"Q {num_questoin}"):
            st.write(questoin)
            answer = st.text_input("Answer")
            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if test and not test(answer):
                st.write("try again... answer not match")
            elif submitted and answer:
                write_answer.add_answer(answer, num_questoin)

    def test_code_by_re(pattern: re.Pattern) -> Callable[[str], bool]:
        def f(code: str) -> bool:
            f_pattern = re.compile(pattern)
            return bool(f_pattern.match(code))
        return f
