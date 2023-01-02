import sys
import os
import streamlit as st
import pandas as pd
from pages.Utilities.Utilities import WriteAnswers, DataLoader, Questions, Utilities
df_status = DataLoader.df_status
df_names = DataLoader.df_names
utilities_path = DataLoader.utilities_path


st.set_page_config(page_title="Multiplication table", page_icon="🔢")
name = Utilities.enter_name()
write_answers = WriteAnswers(name, utilities_path / "status.csv")
st.title(f"{name} Welcome to Multiplication table Ex")
df_status = DataLoader.load_df_status()
st.dataframe(df_status.loc[df_status["NAME"] ==
                           name], use_container_width=True)

Questions.execute_question(1, '''Printing the numbers 1 through 10: 
     _remember_ `range(x,y)` run from x to y-1''',
                           write_answer=write_answers
                           )

Questions.execute_question(2, """
Print the numbers from 1-10 in one line, use the function `print_row()` a we provided you.
This function prints all the numbers in a row
""",
                           code='''
print_row = lambda x: print(x,end=" ") 

#exemple you sould delete it
print("hello")
print("world")

print_row("hello") 
print_row("world")
''',
                           write_answer=write_answers
                           )

Questions.execute_question(3, """Print all the numbers $i^2$  numbers 1 through 10 in one line, use the function `print_row()`:
```python
1 4 9 ...
```
""",
                           code='''print_row = lambda x: print(x,end=" ")
                           ''',
                           write_answer=write_answers
                           )

Questions.execute_question(4, '''
Print the numbers $1*3$ to $10*3$ in one line
```python
3 6 12 ...
```
''',
                           code='''print_row = lambda x: print(x,end=" ")
                           ''',
                           write_answer=write_answers
                           )
Questions.execute_question(5, '''
Take the loop from the previous exercise and place it inside a loop that ran 3 times, so that it will be printed 3 times,use for in for
```python
3...30 3 ... 30 3...30 
```
''',
                           code='''print_row = lambda x: print(x,end=" ")
                           ''',
                           write_answer=write_answers
                           )
Questions.execute_question(6, "P",
                           code='my_string = "Hello, world!"',
                           write_answer=write_answers)
Questions.execute_question(7, '''Printing the numbers 0 through 29,
                                         but only the ones that are multiples of 3: _using `range()`_''',
                           write_answer=write_answers)
Questions.execute_question(8, '''Printing the elements of a list of numbers,
                                        but only the ones that are divisible by both 2 and 3:''',
                           code='my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13]',
                           write_answer=write_answers)
