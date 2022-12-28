import pandas as pd
from typing import List, Tuple, Callable, TextIO
import streamlit as st
from pathlib import Path


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

    def __init__(self, name: str, file_name: Path, test_data_fn: Callable = None) -> None:
        assert name in Utility.df_names["NAME"].values, "Name must be in names"
        self.name = name
        self.file_name = file_name
        self.test_data = test_data_fn
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
        if self.test_data and not self.test_data(answer):
            return "faild test...."
        df = pd.read_csv(self.file_name, skipinitialspace=True, dtype="string")
        df.loc[df["NAME"] == self.name, str(num_answers)] = answer
        df.to_csv(self.file_name, index=False)
        st.write("good job!")
