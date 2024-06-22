import streamlit as st

from pages_backend.practice.base_practice import BasePractice
from pages_backend.practice.practice_factory import get_practice
from pages_backend.practice.practice_type import PracticeType

practice = BasePractice()

st.set_page_config(
    page_title="Practice",
    page_icon="🔍",
)

practice_type = st.selectbox(
    label="Select Practice Type",
    options=[practice_type.value for practice_type in PracticeType],
    on_change=practice.regenerate
)

practice = get_practice(practice_type)

practice.practice()
