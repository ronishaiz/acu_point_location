from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from random import shuffle
from typing import List, Dict

import streamlit as st

from pages_backend.utils import format_displayable_object


@dataclass
class Question:

    _answer: str
    _question_str: str

    @property
    def answer(self) -> str:
        return self._answer

    @property
    def question_str(self) -> str:
        return self._question_str

    @classmethod
    def generate(cls, questions_to_answers: Dict[str, str], num_questions_to_generate: int) -> List['Question']:

        if num_questions_to_generate > len(questions_to_answers):
            raise ValueError("Were asked to generate more questions than those that exist")

        questions = [cls(_answer=str(format_displayable_object(answer)), _question_str=str(question))
                     for question, answer in questions_to_answers.items()]

        shuffle(questions)

        questions = questions[:num_questions_to_generate]

        return questions


@dataclass
class DisplayableQuestion(metaclass=ABCMeta):

    _question: Question

    @abstractmethod
    def display_question_and_get_answer(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def generate(cls, questions_to_answers: dict, num_questions_to_generate: int) -> List['DisplayableQuestion']:
        pass

    def display(self):
        answer = self.display_question_and_get_answer()

        st.button("Submit", key="Submit Answer", on_click=lambda: self.submit_answer(answer))

    def submit_answer(self, answer: str):
        if answer == self._question.answer:
            st.write("Correct! :white_check_mark:")

        else:
            st.write("Wrong! :x:")
            st.write(f"The Correct Answer: {self._question.answer}")
