from backend.enums import PointCharacter
from backend.meridians.meridian import ALL_POINTS
from pages_backend.flashcards.flashcard import FlashCard
import streamlit as st
import pandas as pd

character_groups = {character: [point for point in ALL_POINTS if character in point.characters] for character in PointCharacter}


def show_character_group(character_str: str):
    character = PointCharacter(character_str)
    points = character_groups[character]
    st.header(character.value)

    for point in points:
        st.button(point.identifier, on_click=FlashCard(point).show_content, key=f'{point.identifier}_{character.name}')


def show_download_big_picture():
    big_picture_df_key = 'big_picture_df'

    if big_picture_df_key not in st.session_state:
        st.session_state[big_picture_df_key] = get_big_picture_df()

    st.download_button(
        label="Download The Big Picture",
        data=convert_df(st.session_state[big_picture_df_key]),
        file_name="the_big_picture.csv",
        mime="text/csv",
    )


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")


def get_big_picture_df() -> pd.DataFrame:
    return pd.concat([pd.DataFrame({character.value: [point.identifier for point in points]}) for character, points in character_groups.items()],
                     axis=1)
