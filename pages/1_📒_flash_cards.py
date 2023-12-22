import streamlit as st

from backend.enums import Organ
from backend.meridians.meridian import ALL_POINTS, ALL_MERIDIANS, get_meridian_by_organ
from pages_backend.flashcards.flashcard import FlashCard, FlashCardStack


def restack(sort: bool = False):
    if 'stack' in st.session_state:
        st.session_state.pop('stack')

    st.session_state['sort'] = sort


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

if flashcard_topic == 'Points':
    meridian_selection = st.selectbox('Choose Meridian', ['ALL'] + [meridian.organ.value for meridian in ALL_MERIDIANS], on_change=restack)
    flashcard_objects = ALL_POINTS if meridian_selection == 'ALL' else get_meridian_by_organ(Organ(meridian_selection)).points

else:
    flashcard_objects = ALL_MERIDIANS

flashcards = [FlashCard(flashcard_object) for flashcard_object in flashcard_objects]

st.button('Shuffle', on_click=restack)
st.button('Sort', on_click=lambda: restack(True))

if 'stack' not in st.session_state:
    st.session_state['stack'] = FlashCardStack(flashcards, st.session_state.get('sort', False))

show_flashcards()
