import sys
import os
import streamlit as st
import pandas as pd
import numpy as np
from streamlit import session_state as ses
from __init__ import WriteAnswers, Questions, Utilities, DataLoader

names_df: DataLoader = DataLoader("names_and_answers/names.csv")
status_df: DataLoader = DataLoader("names_and_answers/answers_ex1.csv")

st.set_page_config(
    page_title="Complexity", page_icon="🔢", initial_sidebar_state="collapsed"
)
name = Utilities.enter_name(names_df)
write_answers: WriteAnswers = WriteAnswers(name, status_df)
st.title(f"{name} Welcome to Luhn_algoritem exercise")
st.dataframe(
    status_df.df.loc[status_df.df["NAME"] == name].replace([np.nan, " "], "🤔"),
    use_container_width=True,
)


Questions.execute_question(
    1,
    r"""
כיתבו פונקציה 
`sum_ID_number(id)`
שמקבלת 
`id:str`
מספר תעודת זהות, עוברת על כל הספרות שבו וסוכומת אותם. 
שימו לב - הספרות הם מסוג 
`str`
ולא ניתן לסכום אותם ככה. 
    """,
    code="""\ndef sum_ID_number(id):\n\tpass\n\n """,
    write_answer=write_answers,
)


Questions.execute_question(
    2,
    r"""
כיתבו פונקציה 
`special_sum_ID_number(id)`
שמקבלת 
`id:str`
מספר תעודת זהות, עוברת על כל הספרות שלו וסוכמת בצורה הבאה:
אם הסיפרה היא _במקום_ אי זוגי - סוכמים את הסיפרה כמו שהיא, אחרת - כלומר הסיפרה במקום זוגי - מכפילים אותה פי שתיים וסוכמים
""",
    code="""\ndef special_sum_ID_number(id):\n\tpass""",
    write_answer=write_answers,
)


Questions.execute_question(
    3,
    r"""
כיתבו פונקציה בשם 
`sum_digitis(n)`
שמקבלת מספר 
`n:int`
 ומחזירה את סכום הספרות שלו. 
השתמשו ב 
`n%10` 
בשביל לדעת את סיפרת האחדות של המספר
וב
`n//10` 
בשביל לדעת את סיפרת העשרות של המספר
 """,
    code="\ndef sum_digits(n):\n\tpass",
    write_answer=write_answers,
)


Questions.execute_question(
    4,
    r"""
שלבו את הפונקציות 
`special_sum_ID_number`
ו
`sum_digitis`
לפונקציה אחת
`Luhn_sum_digits(id)`
שמקבלת 
`id:n` 
מספר תעודת זהות, 
ומחזירה את הסכום הספרות שלו לפי אלגוריתם 
Luhn
כלומר - לכל סיפרה, אם היא במקום אי זוגי סוכמים אותה כמו שהיא, אחרת - כלומר היא במקום זוגי
מכפילים אותה פי שתיים ומעברים את המספר הזה לפונקציה 
`sum_digitis`
שסוכמת לפי הספרות של המכפלה
ואת המספר הזה סוכמים. 
""",
    code="\ndef Luhn_sum_digits(id):\n\tpass",
    write_answer=write_answers,
)


Questions.execute_question(
    5,
    r"""
השתמשו בפונקציה הקודמת 
`Luhn_sum_digits`
בשביל לכתוב את האלגוריתם למציאת ספרת ביקורת.
לאחר שיש לכם את סכום הספרות בצורה הנדרשת
עליכם למצוא את סיפרת האחדות מהסכום, 
נקרא למספר הזה 
`s`
סיפרת הביקורת היא 
`10-s`
כיתבו פונקציה 
`control_digit(ID):`
שמקבלת מספר זהות 
`ID:str`
ומזירה את סיפרת הביקורת שלו
    """,
    code="\ndef def control_digit(ID):\n\tpass",
    write_answer=write_answers,
)

