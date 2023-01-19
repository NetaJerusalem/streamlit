import os
import random
import pandas as pd
from pandas import DataFrame
import re
from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Tuple,
    Callable,
    TextIO,
    Final,
    Type,
    Union,
    Iterator,
)
import streamlit as st
from streamlit import session_state as ses
from pathlib import Path
import subprocess
from streamlit_ace import st_ace
from collections import Counter, namedtuple
import time

PASSWORD: Literal["13245"] = "13245"
dfLoc = namedtuple("dfLoc", ("row", "column"))
SAD_EOMJI: set[str] = {"😵‍💫", "😢", "😭", "😰", "😩"}
HAPPY_EMOJI: set[str] = {"😀", "😁", "😆", "😘", "😍", "🥰", "🙂", "😚"}
LOAD_PATTERN: str = r"^##\d+(.|\n)*?(?=##\d+)"  # https://regex101.com/r/Tphpe0/1
TOP_ROW_PATTERN: str = r"^##\d+.*(?=\n)"  # https://regex101.com/r/xMqjlJ/1
CLINE_ANSWER_PATTERN: str = r"\s+|\"|\'"


def _random_eomji(emojis: set[str]) -> Callable[[], str]:
    """
    return function that randomly returns emoji

    Args:
        emojis (set[str]): list of emojis

    Returns:
        Callable[[None],str]: function that returns random emoji with spaces!!
    """

    def f():
        return " " + random.choice(list(emojis))

    return f


sad_eomji: Callable[[], str] = _random_eomji(SAD_EOMJI)
happy_eomji: Callable[[], str] = _random_eomji(HAPPY_EMOJI)


class DataLoader:
    def __init__(self, name: str, path: Optional[Path] = None) -> None:
        """
        initial data loader instance, connected to csv file
        can be used to write data (answers) to a file

        Args:
            name (str): name of file to load, file most be CSV
            path (Optional[Path], optional): if is path find the file in path
            otherwise find file in Utilitis folder. Defaults to None.
        """
        if path:
            self.path: Path = path / name
        else:
            self.path = Path(__file__).parents[0] / name
        self.df: DataFrame = pd.read_csv(self.path, skipinitialspace=True, dtype="string")

    def reload(self) -> DataFrame:
        """
        relad data from file

        Returns:
            DataFrame: new data frame that reload
        """
        self.df = pd.read_csv(self.path)
        return self.df

    def write(
        self,
        data: Union[int, float, str],
        loc: Union[dfLoc, Tuple[str, str]],
    ) -> DataFrame:
        """
        write data to file, and return the updated file

        Args:
            data (Union[int, float, str]): data to write
            loc (Union[dfLoc, Tuple[str, str]]): location to write, given by - row, colomn

        Returns:
            DataFrame: updated file
        """
        if type(loc) != dfLoc:
            loc = dfLoc(loc[0], loc[1])
        # type: ignore
        self.df.at[loc.row, loc.column] = data
        self.df.to_csv(self.path, index=False)
        return self.reload()

    def write_by_name(
        self,
        data: Union[int, float, str],
        loc: Union[dfLoc, Tuple[str, str]],
    ) -> DataFrame:
        if type(loc) != dfLoc:
            loc = dfLoc(loc[0], loc[1])
        # type: ignore
        self.df.loc[self.df["NAME"] == loc.row, loc.column] = data
        self.df.to_csv(self.path, index=False)
        return self.reload()

    def show_df(self, fancy: Optional[Literal["wide"]] = None) -> None:
        """
        show the dataFrame in stteamlit

        Args:
            fancy (Literal['wide'] | None, optional): which way show the data. Defaults to None.
        """
        if fancy == "wide":
            st.dataframe(
                self.df.style.set_table_styles(
                    dict(selector="th", props=[("max-width", "70px")])
                ),
                use_container_width=True,
            )
        else:
            st.dataframe(self.df)

    def add_name(self, name: str) -> DataFrame:
        if name not in self.reload()["NAME"].values:
            self.df = pd.concat([self.df, pd.DataFrame([{"NAME": name}])])
            self.df.to_csv(self.path, index=False)
        return self.reload()

    def download(self) -> None:
        """
        create a button that allowed the admin to download status
        """
        file_name = os.path.basename(self.path)
        if ses.user_name == "admin":
            st.download_button(f"download {file_name}", self.df.to_csv(), file_name)


class WriteAnswers:
    """
    Write the answer to CSV file
    """

    def __init__(self, name: str, file: DataLoader) -> None:
        self.name: str = name
        self.file: DataLoader = file
        self.file.add_name(name)
        self.set_name: str = self.file.path.name

    def add_answer(self, answer: str, num_answers: int) -> None:
        """
        write answers to CSV file
        Arg:
        answer: str - data to write to CSV file
        num_answers: int - number of questions to write
        """
        self.file.write_by_name(answer, dfLoc(self.name, str(num_answers)))


class Questions:
    @staticmethod
    def execute_question(
        num_questoin: int,
        questoin: str,
        test_fn: Optional[Callable[[str], bool]] = None,
        write_answer: Optional[WriteAnswers] = None,
        code: str = "",
        show_output: bool = True,
        title: str = "",
        add_test_code: str = "",
        caption: str = "",
    ) -> None:
        """
        Create a new code question where the user is presented with a description of the task and a code editor
        to answer the question.
        Optionally, initial code can be provided and/or test code can be added to evaluate the answer.
        A function can also be supplied to check if the answer is correct.

        Args:
            num_question (int): The unique number for the question.
            question (str): The description of the task.
            test_fn (Callable[[str], bool], optional): A function to test the answer. Defaults to None.
            write_answer (WriteAnswers, optional): An object with a method `add_answer(answer, user_name, question_num)` to write the answer. Defaults to None.
            code (str, optional): Code to display in the code editor at the start. Defaults to "".
            show_output (bool, optional): Whether to show the output of code execution. Defaults to True.
            title (str, optional): The title of the question. If empty, the number will be set to `num_question`. Defaults to "".
            add_test_code (str, optional): Additional test code to add after the answer. Defaults to "".
            caption (str, optional): A caption to display in the question. Defaults to "".
        """

        # if the title is None
        form_title: str = title or f"Question {num_questoin}"
        file_name: str = Path(__file__).name
        with st.form(f"{form_title}_{file_name}"):
            st.subheader(form_title)
            for line in questoin.splitlines():
                # deplay differnt line in different write,
                # (is the only way to display different lines in st.write)
                st.write(line)
            if caption:
                st.caption(caption)
            # take the code and remove provided code from the answer
            answer: str = st_ace(value=code, language="python", auto_update=True)

            # evaluate the code
            if st.form_submit_button("Submit"):
                if add_test_code:  # add code after answer
                    answer = answer + add_test_code
                # evaluate the answer
                output: str = subprocess.run(
                    ["python", "-c", answer],
                    capture_output=True,
                    text=True,
                ).stdout
                if show_output:
                    st.code(output)
                if test_fn and not test_fn(output):
                    st.write("try again... code not match")
                if write_answer:
                    write_answer.add_answer(answer.replace(code, ""), num_questoin)

    @staticmethod
    def quick_questions(
        name: str,
        num_questoin: int,
        reload: bool = False,
        seconds: int = 40,
        write_answer: Optional[WriteAnswers] = None,
        show_answers: bool = False,
    ) -> None:
        """
        This function creates a "quick questions" form for a code file in a specific format, as specified in the README file.
        The function compares the user's input (answer) to the true output of the code snippet,
        ignoring spaces, line breaks, quotation marks, doubles or singles.

        Args:
            name (str): The name of the file from which the code snippet is uploaded. The file must conform to the format specified in the README file.
            key (Optional[str], optional): When creating multiple quick questions, this argument specifies a unique key for each question.
            reload (bool, optional): When set to True, deletes all progress and starts the game from the beginning. Defaults to False.
            seconds (int, optional): The amount of time for each question. Defaults to 40.
            show_answers (bool, optional): When set to True, displays the current answer, useful for testing. Defaults to False.
        """
        # init session_stete (ses) variables
        file_name: str = Path(__file__).name
        key: str = f"quick_questions_{num_questoin}_{file_name}"

        def __init_session_stete() -> None:
            path: Path = Path(__file__).parents[0] / name
            ses.codes = Utilities.load_codes(path)
            ses.bar = 0
            ses.successes_counter = ""
            ses.sub_pattern = re.compile(r"\s+|\"|\'")
            ses.successes_f = False
            ses.sleep_time = seconds / 100
            ses[key] = "wait"
            ses.start_time = time.time()

        if key not in ses or reload:
            __init_session_stete()
        if ses[key] == "wait":
            if st.button("start 🏃‍♀️"):
                ses[key] = "running"
                st.experimental_rerun()

        # init placeholder for components
        q = st.container()
        code_place = q.empty()
        input_place = q.empty()
        bar_place = q.empty().progress(ses.bar)
        successes = q.empty()

        # main loop, run until finished all code snippets
        while len(ses.codes) > 1 and ses[key] == "running":
            if ses.bar == 100:  # bar is 100 when answer is correct or timeout
                ses.successes_counter += happy_eomji() if ses.successes_f else sad_eomji()
                ses.codes.pop(0)
                ses.bar = 0
                ses.successes_f = False
                input_place.empty()

            # write the amout of successes
            successes.write(f"# {ses.successes_counter}")
            answer = input_place.text_input(
                "What the output of this code?",
                key=f"{file_name}_{str(len(ses.codes))}",
            )
            code, output = ses.codes[0]["code"], ses.codes[0]["output"]
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

        if ses[key] == "running":
            finish_time: int = int(time.time() - ses.start_time)
            count_successes: int = len(re.findall("[😀😁😆😘😍🥰🙂😚]", ses.successes_counter))
            ses.successes_counter = f"You answered {count_successes} correct answers in the time of: {finish_time} seconds"
            if write_answer:
                write_answer.add_answer(
                    f"correct answers:{count_successes}, time: {finish_time}",
                    num_questoin,
                )
            ses[key] = "finished"

        successes.write(f"## {ses.successes_counter}")

    @staticmethod
    def quick_questions_no_bar(
        name: str,
        num_questoin: int,
        reload: bool = False,
        write_answer: Optional[WriteAnswers] = None,
        show_answers: bool = False,
        show_time: bool = False,
        enable_next: bool = True,
    ) -> None:
        """
        This function creates a "quick questions" form for a code file in a specific format, as specified in the README file.
        The function compares the user's input (answer) to the true output of the code snippet,
        ignoring spaces, line breaks, quotation marks, doubles or singles.

        Args:
            name (str): The name of the file from which the code snippet is uploaded. The file must conform to the format specified in the README file.
            key (Optional[str], optional): When creating multiple quick questions, this argument specifies a unique key for each question.
            reload (bool, optional): When set to True, deletes all progress and starts the game from the beginning. Defaults to False.
            show_answers (bool, optional): When set to True, displays the current answer, useful for testing. Defaults to False.
            show_time (bool, optional): When set to True, after finis all questions display the time take to answer all questoins. Defaults to False.
        """
        # init session_stete (ses) variables
        file_name: str = Path(__file__).name
        key_set: str = f"quick_questions_no_bar{num_questoin}_{file_name}"

        def __init_session_stete() -> None:
            path: Path = Path(__file__).parents[0] / name
            ses.codes = Utilities.load_codes(path)
            ses.successes_counter = ""
            ses.sub_pattern = re.compile(CLINE_ANSWER_PATTERN)
            ses.successes_f = False
            ses.next = False  #
            ses[key_set] = "wait"
            ses.start_time = time.time()

        def __next_question() -> None:
            ses.successes_counter += happy_eomji() if ses.successes_f else sad_eomji()
            ses.codes.pop(0)
            ses.successes_f = False
            ses.next = False
            input_place.empty()

        def __check_answer() -> None:
            if output == ses.sub_pattern.sub("", ses[key_q].casefold()):
                ses.successes_f = True
                __next_question()

        if key_set not in ses or reload:
            __init_session_stete()
        if ses[key_set] == "wait":
            if st.button("start 🏃‍♀️"):
                ses[key_set] = "running"
                st.experimental_rerun()
            st.stop()

        # init placeholder for components
        q = st.container()
        code_place = q.empty()
        input_place = q.empty()
        successes = q.empty()

        # main loop, run until finished all code snippets
        if len(ses.codes) > 1 and ses[key_set] == "running":
            if enable_next:
                q.button("next", on_click=__next_question)
            # write the amout of successes
            key_q = f"{file_name}_{str(len(ses.codes))}"
            code, output = ses.codes[0]["code"], ses.codes[0]["output"]
            code_place.code(code, language="python")
            input_place.text_input(
                "What the output of this code?",
                key=key_q,
                on_change=__check_answer,
            )

            if show_answers:  # for testing show the current answer
                successes.write(f"the current answer is `{output}`")

        elif ses[key_set] == "running":
            finish_time: int = int(time.time() - ses.start_time)
            count_successes: int = len(re.findall("[😀😁😆😘😍🥰🙂😚]", ses.successes_counter))
            if show_time:
                ses.successes_counter = f"You answered {count_successes} correct answers in the time of: {finish_time} seconds"
            else:
                ses.successes_counter = f"You answered {count_successes} correct answers"

            if write_answer:
                write_answer.add_answer(
                    f"correct answers:{count_successes}, time: {finish_time}",
                    num_questoin,
                )
            ses[key_set] = "finished"

        successes.write(f"## {ses.successes_counter}")


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
                "Enter your username", autocomplete="name"
            )
            # enter for admin
            if user_name == "admin":
                password_field = st.empty()
                password: str = password_field.text_input(
                    "Enter password", type="password"
                )
                if password == PASSWORD:
                    ses.user_name = user_name
                    plaseholder.success(f"{user_name} Welcome to our system")
                    password_field.empty()
                    return user_name
            # entner for user
            elif user_name in names.df["NAME"].values:
                ses.user_name = user_name
                plaseholder.success(f"{user_name} Welcome to our system")
                return user_name
            # if the user is not in the names list
            elif user_name:
                st.write(
                    "your name not in names...\n enter your name like codebord name\n find your name in this list"
                )
                st.dataframe(names.df["NAME"])

            st.stop()
        else:
            return ses.user_name

    @staticmethod
    def first_time_message(msg: str) -> None:
        page_name: str = Path(__file__).name
        if page_name + "_msg" not in ses:
            ses[page_name + "_msg"] = True
            st.write(msg)
            st.button("אוקיי, הבנתי")
            st.stop()

    @staticmethod
    def load_codes(
        path,
        load_pattern: str = LOAD_PATTERN,
        remove_pattern: str = CLINE_ANSWER_PATTERN,
        data_pattern: str = TOP_ROW_PATTERN,
    ) -> List[Dict[str, Any]]:
        """
        Load code snippets from file using a specified regex pattern to separate the file into several snippets,
        and another pattern to remove spaces and newlines from the output.

        Args:
            path (str): Path to the file to load.
            load_pattern (str, optional): Regex pattern to separate the file into code snippets. Defaults to LOAD_PATTERN.
            remove_pattern (str, optional): Regex pattern to remove from the output code. Defaults to REMOVE_PATTERN.

        Raises:
            RuntimeError: If the code snippet raises an exception or does not print anything.

        Returns:
            List[Tuple[str, str]]: A list of tuples containing the code snippet and the desired output.
        """
        # regex pattern to split questions form file
        _load_pattern: re.Pattern[str] = re.compile(load_pattern, re.M)
        _remove_pattern: re.Pattern[str] = re.compile(remove_pattern)
        _data_pattern: re.Pattern[str] = re.compile(data_pattern, re.M)
        ret: List[Dict[str, Any]] = []

        with open(path) as f:  # Iterate through code snippets
            iter_codes: Iterator[re.Match[str]] = _load_pattern.finditer(f.read())
            for match_code in iter_codes:
                _code: str = match_code.group()
                # Run code and check if it prints something
                compile: subprocess.CompletedProcess[str] = subprocess.run(
                    ["python", "-c", _code],
                    capture_output=True,
                    text=True,
                )
                # If code does not print something, or there was an error in running the code
                #  (even if it printed something)
                if not compile.stdout or compile.returncode:
                    raise RuntimeError("Execute code filed, code:{}".format(_code))
                # Lower all characters and remove spaces and newlines
                _output: str = _remove_pattern.sub("", compile.stdout.casefold())
                _data_match = _data_pattern.match(_code)
                if _data_match:
                    _data = _data_match.group()
                    _code = _data_pattern.sub("", _code)
                ret.append({"code": _code, "output": _output})
        return ret

    @staticmethod
    def test_code_by_re(pattern: str) -> Callable[[str], bool]:
        """
        return function that checks if some text matches to a given pattern

        Args:
            pattern (str): desaired pattern to check

        Returns:
            Callable[[str], bool]: function that returns true if code match to pattern else false
        """

        def f(code: str) -> bool:
            f_pattern = re.compile(pattern)
            return bool(f_pattern.match(code))

        return f
