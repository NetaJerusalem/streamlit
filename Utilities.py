import pandas as pd
from typing import List, Tuple, Callable, TextIO


class AddAnswer:
    def __init__(self, out_strem: str, test_data_fn: Callable = None) -> None:
        self.df = pd.read_csv(out_strem) 
        if test_data_fn is not None:
            self.test_data = test_data_fn

    def add_answer(self, answer: str, num_answers: int):
        if self.test_data and not self.test_data(answer):
            raise ValueError("test data failed")
        self.out_strem.write(answer)

