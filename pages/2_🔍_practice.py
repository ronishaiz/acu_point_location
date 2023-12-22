import streamlit as st

from pages_backend.coming_soon_page import coming_soon_page

st.set_page_config(
    page_title="Practice",
    page_icon="🔍",
)

coming_soon_page()
