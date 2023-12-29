import streamlit as st

from pages_backend.practice.practice_type import PracticeType
from pages_backend.practice.random_choice_practice import random_choice_practice

st.set_page_config(
    page_title="Practice",
    page_icon="🔍",
)

practice_type = st.selectbox(
    label="Select Practice Type",
    options=[PracticeType.random_choice.value]
)

if practice_type == PracticeType.random_choice.value:
    random_choice_practice()
