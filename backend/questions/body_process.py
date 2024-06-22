import os.path
from dataclasses import dataclass
from typing import List, Dict

from backend.enums import Organ
from backend.questions.question import MultipleAnswerDisplayableQuestion, MultipleAnswerQuestion
import streamlit as st

body_process_pictures_folder = os.path.join(os.path.dirname(__file__), 'banks', 'body_process_pictures')


@dataclass
class BodyProcess:

    _picture_file_name: str
    _organ_to_related_points: Dict[Organ, Dict[str, str]]

    @property
    def picture_file_name(self) -> str:
        return self._picture_file_name

    @property
    def picture_path(self):
        return os.path.join(body_process_pictures_folder, self.picture_file_name)

    @property
    def organs(self) -> List[Organ]:
        return list(self._organ_to_related_points.keys())

    @property
    def organ_to_related_points(self) -> Dict[Organ, Dict[str, str]]:
        return self._organ_to_related_points

    @property
    def process_name(self):
        without_filetype = self.picture_file_name.split('.')[0]
        words = without_filetype.split('_')
        words = [word.capitalize() for word in words]
        return " ".join(words)


class BodyProcessQuestion(MultipleAnswerDisplayableQuestion):

    @classmethod
    def generate(cls, questions_to_answers: Dict[str, Dict[str, str]], num_questions_to_generate: int) -> List['BodyProcessQuestion']:
        return [cls(question) for question in MultipleAnswerQuestion.generate(questions_to_answers, num_questions_to_generate)]

    def display_question_and_get_answer(self) -> str:
        st.button("Show All Points", on_click=self.show_answers)
        return st.text_input(self._question.question_str).upper().replace(' ', '').replace('_', '')
