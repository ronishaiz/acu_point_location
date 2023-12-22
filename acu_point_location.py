import streamlit as st

st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
)

st.write("# Welcome to Acu-Point Location! 👋")

st.sidebar.success("Select your study plan")

st.markdown(
    """
    Acu-Point Location is meant to help students memorize and acurately recall the properties of
    Chinese Medicine acupuncture points.
    Made on-going, by a student currently learning, so the Meridians will be uploaded to the site gradually,
    in the course of 2024-2025.
    **👈 Select your study plan from the sidebar** to start learning!
    
    ### Want to contribute?
    - See Github: https://github.com/ronishaiz/acu_point_location
    - Found a mistake? Please let me know!! 😇
"""
)
