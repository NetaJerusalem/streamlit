import os
import random
import pandas as pd
from pandas import DataFrame
import re
from typing import List, Literal, Optional, Tuple, Callable, TextIO, Final, Type, Union, Iterator
import streamlit as st
from streamlit import session_state as ses
from pathlib import Path
import subprocess
from streamlit_ace import st_ace
from collections import namedtuple
import time

PASSWORD: Literal["13245"] = "13245"
dfLoc = namedtuple("dfLoc", ("row", "column"))
SAD_EOMJI: set[str] = {"😵‍💫", "😶‍🌫️", "😢", "😭", "😰", "😩"}
HAPPY_EMOJI: set[str] = {"😀", "😁", "😆", "😘", "😍", "🥰", "🙂", "😚"}


def _random_eomji(emojis: set[str]) -> Callable[[], str]:
    '''
    return function that randomly returns emoji

    Args:
        emojis (set[str]): list of emojis

    Returns:
        Callable[[None],str]: function that returns random emoji with spaces!!
    '''
    def f():
        return " " + random.choice(list(emojis))
    return f


sad_eomji = _random_eomji(SAD_EOMJI)
happy_eomji = _random_eomji(HAPPY_EMOJI)


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
        create a button that allowed the admin to download status
        '''
        file_name = os.path.basename(self.path)
        if ses.user_name == 'admin':
            st.download_button(f'download {file_name}',
                               self.df.to_csv(), file_name)


class WriteAnswers:
    """
    Write the answer to CSV file
    """

    def __init__(self, name: str, file: DataLoader) -> None:
        self.name: str = name
        self.file: DataLoader = file
        self.file.add_name(name)

    def add_answer(self,  answer: str, num_answers: int) -> None:
        """
        write answers to CSV file
        Arg:
        answer: str - data to write to CSV file
        num_answers: int - number of questions to write
        """
        self.file.write_by_name(answer, dfLoc(self.name, str(num_answers)))


class Questions:

    @staticmethod
    def execute_question(num_questoin: int, questoin: str, test_fn: Optional[Callable[[str], bool]] = None,
                         write_answer: Optional[WriteAnswers] = None, code: str = "", show_output: bool = True,
                         title: str = "", add_test_code: str = "", caption: str = ""):
        # if the title is None
        form_title = title or f"Question {num_questoin}"
        with st.form(form_title):

            st.subheader(form_title)
            st.write(questoin)
            if caption:
                st.caption(caption)
            # take the code and remove provided code from the answer
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
    def question(num_questoin: int, question: str, test: Optional[Callable[[str], bool]] = None, write_answer: Optional[WriteAnswers] = None, title: str = ""):
        with st.form(f"Q {num_questoin}"):
            st.write(question)
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
    def quick_questions(name: str, key: Optional[str] = None, reload: bool = False, seconds: int = 40, write_answer: Optional[WriteAnswers] = None, show_answers: bool = False) -> None:
        '''
        This function creates a "quick questions" form for a code file in a specific format, as specified in the README file. 
        The function compares the user's input (answer) to the true output of the code snippet, 
        ignoring spaces, line breaks, quotation marks, doubles or singles. 

        Args:
            name (str): The name of the file from which the code snippet is uploaded. The file must conform to the format specified in the README file.
            key (Optional[str], optional): When creating multiple quick questions, this argument specifies a unique key for each question.
            reload (bool, optional): When set to True, deletes all progress and starts the game from the beginning. Defaults to False.
            seconds (int, optional): The amount of time for each question. Defaults to 40.
            show_answers (bool, optional): When set to True, displays the current answer, useful for testing. Defaults to False.
        '''
        # init session_stete (ses) variables
        def __init_session_stete():
            pattern_load = re.compile(r'#[1-9](.|\n[^#])*')
            path: Path = Path(__file__).parents[0] / name
            ses.codes = []
            ses.bar = 0
            ses.successes_counter = ""
            ses.sub_pattern = re.compile(r'\s+|\"|\'')
            ses.successes_f = False
            ses.sleep_time = seconds/100
            ses.start_time = time.time()
            with open(path) as f:  # load all questions form file
                iter_codes: Iterator[re.Match[str]
                                     ] = pattern_load.finditer(f.read())
                for match_code in iter_codes:
                    _code: str = match_code.group()
                    # run code and check if it print something
                    compile: subprocess.CompletedProcess[str] = subprocess.run(
                        ['python', '-c', _code], capture_output=True, text=True)
                    if not compile.stdout or compile.returncode:
                        raise RuntimeError(
                            "Execute code filed, code:{}".format(_code))
                    _outpot: str = ses.sub_pattern.sub(
                        "", compile.stdout.casefold())
                    ses.codes.append((_code, _outpot))

        if "codes" not in ses or reload:
            __init_session_stete()
        # init placeholder for components
        q = st.container()
        code_place = q.empty()
        input_place = q.empty()
        bar_place = q.empty().progress(ses.bar)
        successes = q.empty()

        # main loop, run until finished all code snippets
        while len(ses.codes) > 1:
            if ses.bar == 100:  # bar is 100 when answer is correct or timeout
                ses.successes_counter += happy_eomji() if ses.successes_f else sad_eomji()
                ses.codes.pop(0)
                ses.bar = 0
                ses.successes_f = False
                input_place.empty()

            # write the amout of successes
            successes.write(f"# {ses.successes_counter}")
            answer = input_place.text_input(
                "What the output of this code?", key=f"Q{str(8-len(ses.codes))}")
            code, output = ses.codes[0]
            code_place.code(code, language="python")

            if show_answers:  # for testing show the current answer
                successes.write(f"the current answer is `{output}`")
            if answer:
                # eveluat the answer without spaces quotes or newlines
                if output == ses.sub_pattern.sub("", answer.casefold()):
                    ses.successes_f = True
                    ses.bar = 100

            while ses.bar < 100:
                time.sleep(ses.sleep_time)
                ses.bar += 1
                bar_place.progress(ses.bar)
        finish_time: int = int(time.time() - ses.start_time)
        count_successes: int = len(re.findall('[😀😁😆😘😍🥰🙂😚]', ses.successes_counter))

        successes.write(
            f'## You answered {count_successes} correct answers in the time of: {finish_time} seconds')
        if write_answer:
            count_successes = len(re.findall(
                '[😀😁😆😘😍🥰🙂😚]', ses.successes_counter))
            write_answer.add_answer(
                f'correct answers:{count_successes}, time: {finish_time}', 1)


class Utilities:
    """many tools"""
    utilities_path = Path(__file__).parents[0]

    @staticmethod
    def enter_name(names: DataLoader) -> str:
        """avoid load page until the user enters to system
        and register the name in `st.session_state`

        Returns:
            str: name of the user
        """
        if "user_name" not in ses.keys():
            # create a new placeholder for button and input fields
            plaseholder = st.empty()
            user_name: str = plaseholder.text_input(
                "Enter your username", autocomplete="name")
            # enter for admin
            if user_name == "admin":
                password_field = st.empty()
                password: str = password_field.text_input("Enter password")
                if password == PASSWORD:
                    ses.user_name = user_name
                    plaseholder.success(
                        f'{user_name} Welcome to our system')
                    password_field.empty()
                    return user_name
            # entner for user
            elif user_name in names.df["NAME"].values:
                ses.user_name = user_name
                plaseholder.success(f'{user_name} Welcome to our system')
                return user_name
            # if the user is not in the names list
            elif user_name:
                st.write(
                    "your name not in names...\n enter your name like codebord name\n find your name in this list")
                st.dataframe(names.df["NAME"])

            st.stop()
        else:
            return ses.user_name
