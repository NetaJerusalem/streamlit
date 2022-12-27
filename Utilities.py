from typing import List, Tuple,Callable, TextIO


class WriteData:
    def __init__(self, out_strem:TextIO, test_data_fn:Callable=None) -> None:
        self.out_strem = out_strem
        if test_data_fn is not None:
            self.test_data = test_data_fn

    def write(self, data:str):
        if self.test_data and not self.test_data(data):
                raise ValueError("test data failed")
        self.out_strem.write(data)
            

