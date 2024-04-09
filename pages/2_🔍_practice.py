import streamlit as st

from pages_backend.practice.base_practice import BasePractice
from pages_backend.practice.practice_factory import get_practice
from pages_backend.practice.practice_type import PRACTICE_TYPES

practice = BasePractice()

st.set_page_config(
    page_title="Practice",
    page_icon="🔍",
)

practice_type = st.selectbox(
    label="Select Practice Type",
    options=PRACTICE_TYPES,
    on_change=practice.regenerate
)

practice = get_practice(practice_type)

practice.practice()
