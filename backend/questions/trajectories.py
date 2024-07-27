import streamlit as st
from typing import Dict, List

from backend.questions.question import MultipleAnswerDisplayableQuestion, MultipleAnswerQuestion


class TrajectoryQuestion(MultipleAnswerDisplayableQuestion):

    @classmethod
    def generate(cls, questions_to_answers: Dict[str, Dict[str, str]], num_questions_to_generate: int) -> List['TrajectoryQuestion']:
        return [cls(question) for question in MultipleAnswerQuestion.generate(questions_to_answers, num_questions_to_generate)]

    def display_question_and_get_answer(self) -> str:
        st.button("Show All Meridians", on_click=self.show_answers)
        return st.text_input(self._question.question_str).upper().replace(' ', '').replace('_', '')
