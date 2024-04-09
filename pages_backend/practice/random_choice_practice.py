import streamlit as st

from backend.questions.random_choice import RandomChoice
from backend.questions.banks.random_choice_question_banks import Elements, Locations, Characters, Functions, Indications
from pages_backend.practice.base_practice import BasePractice
from pages_backend.utils import Queue


class RandomChoicePractice(BasePractice[RandomChoice]):

    def __init__(self):
        self.label_to_dict = None
        self.selections = None

    def set_practice_setting(self):
        self.label_to_dict = {"Indications": Indications, "Functions": Functions, "Characters": Characters, "Locations": Locations,
                              "Elements": Elements}
        labels = list(self.label_to_dict.keys())

        self.selections = st.multiselect("Select Wanted Question Types", labels, default=labels, on_change=self.regenerate)

    def get_questions_queue(self) -> Queue[RandomChoice]:
        all_questions = []
        for label in self.selections:
            question_to_answer_dict = self.label_to_dict[label]
            all_questions += RandomChoice.generate(questions_to_answers=question_to_answer_dict,
                                                   num_questions_to_generate=len(question_to_answer_dict))

        return Queue[RandomChoice](all_questions)
