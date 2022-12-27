import pandas as pd
from typing import List, Tuple, Callable, TextIO
import streamlit as st
df_names = pd.read_csv("data\\names.csv")


class WriteAnswer:
    def __init__(self, name: str, file_name: str, test_data_fn: Callable = None) -> None:
        assert name in df_names["NAME"].values, "Name must be in names"
        self.name = name
        self.file_name = file_name
        self.test_data = test_data_fn
        df_status = pd.read_csv(self.file_name)
        if self.name not in df_status["NAME"].values:
            df_status = pd.concat(
                [df_status, pd.DataFrame([{"NAME": self.name}])])
            df_status.to_csv(self.file_name,index=False)

    def add_answer(self,  answer: str, num_answers: int):
        if self.test_data and not self.test_data(answer):
            return "faild test...."
        df = pd.read_csv(self.file_name)
        df.loc[df["NAME"] == self.name, str(num_answers)] = answer
        df.to_csv(self.file_name,index=False)
        st.write("good job!") 
