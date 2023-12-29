from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from random import shuffle
from typing import List

import streamlit as st


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
    def generate(cls, questions_to_answers: dict, num_questions_to_generate: int) -> List['Question']:

        questions = []
        question_bank = list(questions_to_answers)

        for _ in range(num_questions_to_generate):

            shuffle(question_bank)

            question_str = question_bank[0]
            answer = questions_to_answers[question_str]
            questions.append(cls(_answer=answer, _question_str=question_str))

        return questions


@dataclass
class DisplayableQuestion(metaclass=ABCMeta):

    _question: Question

    @abstractmethod
    def display(self):
        pass

    def submit_answer(self, answer: str):
        if answer == self._question.answer:
            st.write("Correct! :white_check_mark:")

        else:
            st.write("Wrong! :x:")
            st.write(f"The Correct Answer: {self._question.answer}")
