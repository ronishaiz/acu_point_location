from dataclasses import dataclass
from random import shuffle
from typing import List

from backend.questions.banks.point_location_question_banks import POINT_TO_PICTURE_PATH, QUESTION_STR
from backend.questions.question import DisplayableQuestion, Question

import streamlit as st
from PIL import Image


@dataclass
class PointLocation(DisplayableQuestion):

    _picture_path: str = None

    def display_question_and_get_answer(self) -> str:
        image = Image.open(self._picture_path)

        st.image(image)
        return st.text_input(self._question.question_str).upper().replace(' ', '').replace('_', '')

    @classmethod
    def generate(cls, questions_to_answers: dict, num_questions_to_generate: int) -> List['PointLocation']:

        # all question strings are identical, the question is determined by the image
        questions = [Question(_question_str=QUESTION_STR, _answer=point) for point in questions_to_answers.keys()]
        shuffle(questions)

        return [cls(_question=question, _picture_path=POINT_TO_PICTURE_PATH[question.answer]) for question in questions]
