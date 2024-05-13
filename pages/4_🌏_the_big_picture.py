
import streamlit as st

from pages_backend.the_big_picture.the_big_picture import character_groups, show_character_group, show_download_big_picture

st.set_page_config(
    page_title="The Big Picture",
    page_icon="🌏",
)

show_download_big_picture()

character_str = st.selectbox(
    label="Select Character Type",
    options=[c.value for c in character_groups.keys()],
)

show_character_group(character_str)
