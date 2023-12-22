import streamlit as st

from backend.meridians.meridian import ALL_POINTS, ALL_MERIDIANS
from pages_backend.flashcards.flashcard import FlashCard, FlashCardStack


def restack():
    if 'stack' in st.session_state:
        st.session_state.pop('stack')


def show_flashcards():

    stack = st.session_state['stack']

    hide_content = st.checkbox('Hide Content', value=True, key='hide_flashcard_content')
    show_flashcard(stack.get_top(), hide_content)

    st.button("Next", on_click=lambda: stack.switch(), key="next_flashcard")


def show_flashcard(flashcard: FlashCard, hide_content: bool):
    if hide_content:
        flashcard.show_identifier()
    else:
        flashcard.show_content()


st.set_page_config(
    page_title="Flash Cards",
    page_icon="📒",
)

flashcard_topic = st.selectbox('Select Flashcards Topic', ['Points', 'Meridians'], on_change=restack)
flashcard_objects = ALL_POINTS if flashcard_topic == 'Points' else ALL_MERIDIANS

flashcards = [FlashCard(flashcard_object) for flashcard_object in flashcard_objects]

if 'stack' not in st.session_state:
    st.session_state['stack'] = FlashCardStack(flashcards)

st.button('Shuffle', on_click=restack)

show_flashcards()
