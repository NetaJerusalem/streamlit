import os
import random
import pandas as pd
from pandas import DataFrame
import re
from typing import List, Literal, Optional, Tuple, Callable, TextIO, Final, Type, Union
import streamlit as st
from streamlit import session_state
from pathlib import Path
import subprocess
from streamlit_ace import st_ace
from collections import namedtuple
import time

PASSWORD: Literal["13245"] = "13245"
dfLoc = namedtuple("dfLoc", ("row", "column"))


class DataLoader:

    def __init__(self, name: str, path: Optional[Path] = None) -> None:
        if path:
            self.path: Path = path / name
        else:
            self.path = Path(__file__).parents[0] / name
        self.df: DataFrame = pd.read_csv(
            self.path, skipinitialspace=True, dtype="string")

    def reload(self) -> DataFrame:
        self.df = pd.read_csv(self.path)
        return self.df

    def write(self, data: Union[int, float, str], loc: Union[dfLoc, Tuple[str, str]]) -> DataFrame:
        if type(loc) != dfLoc:
            loc = dfLoc(loc[0], loc[1])
        # type: ignore
        self.df.at[loc.row, loc.column] = data
        self.df.to_csv(self.path, index=False)
        return self.reload()

    def write_by_name(self, data: Union[int, float, str], loc: Union[dfLoc, Tuple[str, str]]) -> DataFrame:
        if type(loc) != dfLoc:
            loc = dfLoc(loc[0], loc[1])
        # type: ignore
        self.df.loc[self.df["NAME"] == loc.row, loc.column] = data
        self.df.to_csv(self.path, index=False)
        return self.reload()

    def show_df(self, fancy: Optional[Literal['wide']] = None) -> None:
        '''
        show the dataFrame in stteamlit

        Args:
            fancy (Literal['wide'] | None, optional): which way show the data. Defaults to None.
        '''
        if fancy == 'wide':
            st.dataframe(self.df.style.set_table_styles(
                dict(selector="th", props=[("max-width", "70px")])), use_container_width=True)
        else:
            st.dataframe(self.df)

    @st.cache
    def add_name(self, name: str) -> DataFrame:
        if name not in self.reload()["NAME"].values:
            self.df = pd.concat(
                [self.df, pd.DataFrame([{"NAME": name}])])
            self.df.to_csv(self.path, index=False)
        return self.reload()

    def download(self) -> None:
        '''
        create button taht allwed the admin download status
        '''
        file_name = os.path.basename(self.path)
        if st.session_state.user_name == 'admin':
            st.download_button(f'download {file_name}',
                               self.df.to_csv(), file_name)


class WriteAnswers:
    """
    Write the answer to csv file
    """

    def __init__(self, name: str, file: DataLoader) -> None:
        self.name: str = name
        self.file: DataLoader = file
        self.file.add_name(name)

    def add_answer(self,  answer: str, num_answers: int) -> None:
        """
        write answer to  csv file,
        Arg:
        answer:str - data to write to csv file
        num_answers:int - number of question to write
        """
        self.file.write_by_name(answer, dfLoc(self.name, str(num_answers)))


class Questions:

    @staticmethod
    def execute_question(num_questoin: int, questoin: str, test_fn: Optional[Callable[[str], bool]] = None,
                         write_answer: Optional[WriteAnswers] = None, code: str = "", show_output: bool = True,
                         title: str = "", add_test_code: str = "", caption: str = ""):
        # if title is not None
        form_title = title or f"Question {num_questoin}"
        with st.form(form_title):

            st.subheader(form_title)
            st.write(questoin)
            if caption:
                st.caption(caption)
            # teke the code and remove provided code form answer
            answer = st_ace(value=code, language="python", auto_update=True)

            # evaluate the code
            if st.form_submit_button("Submit") and answer.replace(code, ""):
                if add_test_code:  # add code after answer
                    answer = answer + add_test_code
                output = subprocess.run(
                    ['python', '-c', answer], capture_output=True, text=True).stdout
                if show_output:
                    st.code(output)
                if test_fn and not test_fn(output):
                    st.write("try again... code not match")
                if write_answer:
                    write_answer.add_answer(
                        answer.replace(code, ""), num_questoin)

    @staticmethod
    def question(num_questoin: int, questoin: str, test: Optional[Callable[[str], bool]] = None, write_answer: Optional[WriteAnswers] = None, title: str = ""):
        with st.form(f"Q {num_questoin}"):
            st.write(questoin)
            answer = st.text_input("Answer")
            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if test and not test(answer):
                st.write("try again... answer not match")
            elif submitted and answer:
                write_answer.add_answer(answer, num_questoin)

    @staticmethod
    def test_code_by_re(pattern: str) -> Callable[[str], bool]:
        def f(code: str) -> bool:
            f_pattern = re.compile(pattern)
            return bool(f_pattern.match(code))
        return f

    @staticmethod
    def quick_questions(name: str,key:Optional[str]=None,reload:bool=False) -> None:
        if "codes" not in session_state.keys() or reload:
            pattern = re.compile(r'#[1-9](.|\n[^#])*')
            path: Path = Path(__file__).parents[0] / name
            with open(path) as f:
                iter_codes = pattern.finditer(f.read())
                session_state.codes = list(text.group() for text in iter_codes)
                session_state.bar = 0
                session_state.successes_counter = ""
        
        code_place = st.empty()
        input_place = st.empty()
        bar_place = st.empty()
        button = st.empty()
        successes = st.empty()
        sabmit = button.button("submit")
        answer = input_place.text_input("enter results")
        bar_place.progress(session_state.bar)
        
        while len(session_state.codes) > 1:
            if session_state.bar == 100:
                session_state.codes.pop(0)
                session_state.bar = 0
            code: str = session_state.codes[0]
            code_place.code(code, language="python")
            output = subprocess.run(
                ['python', '-c', code], capture_output=True, text=True).stdout
            if sabmit and answer:
                st.text(answer+" "+output)
                st.write(answer.replace(" ", "").replace("   ", "") ==
                         output.replace(" ", "").replace("   ", "").replace('"', '').replace("'", ""))
                st.write(type(answer), type(output))
                session_state.successes_counter += " 😎"
                successes.write(f"#{session_state.successes_counter}")
                session_state.bar = 100
                sabmit = False
            while session_state.bar < 100:
                time.sleep(0.25)
                session_state.bar += 1
                bar_place.progress(session_state.bar)


class Utilities:
    """many tools"""
    utilities_path = Path(__file__).parents[0]

    @staticmethod
    def enter_name(names: DataLoader) -> str:
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
                    st.session_state.user_name = user_name
                    plaseholder.success(
                        f'{user_name} Welcome to our system')
                    password_field.empty()
                    return user_name
            # entner for user
            elif user_name in names.df["NAME"].values:
                st.session_state.user_name = user_name
                plaseholder.success(f'{user_name} Welcome to our system')
                return user_name
            # if user not in names list
            elif user_name:
                st.write(
                    "your name not in names...\n enter your name like codebord name\n find your name in this list")
                st.dataframe(names.df["NAME"])

            st.stop()
        else:
            return st.session_state.user_name
