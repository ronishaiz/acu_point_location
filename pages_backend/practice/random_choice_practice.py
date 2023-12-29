import streamlit as st

from backend.questions.random_choice import RandomChoice
from backend.questions.random_choice_question_banks import Elements, Locations, Characters, Functions, Indications
from pages_backend.utils import Queue


def random_choice_practice():
    label_to_dict = {"Indications": Indications, "Functions": Functions, "Characters": Characters, "Locations": Locations, "Elements": Elements}
    labels = list(label_to_dict.keys())

    selections = st.multiselect("Select Wanted Question Types", labels, default=labels, on_change=regenerate)

    if "random_choice_q" not in st.session_state:
        all_questions = []
        for label in selections:
            question_to_answer_dict = label_to_dict[label]
            all_questions += RandomChoice.generate(questions_to_answers=question_to_answer_dict,
                                                   num_questions_to_generate=len(question_to_answer_dict))

        st.session_state["random_choice_q"] = Queue[RandomChoice](all_questions)

    show_questions()


def show_questions():
    q = st.session_state["random_choice_q"]

    q.get_top().display()

    st.button("Previous", on_click=lambda: q.prev(), key="previous_flashcard")
    st.button("Next", on_click=lambda: q.next(), key="next_flashcard")


def regenerate():
    if "random_choice_q" in st.session_state:
        st.session_state.pop("random_choice_q")
