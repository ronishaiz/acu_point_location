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

        cls._validate_num_questions_to_generate(num_questions_to_generate, questions_to_answers)

        questions = [cls(_answer=str(format_displayable_object(answer)), _question_str=str(question))
                     for question, answer in questions_to_answers.items()]

        questions = cls._prepare_questions_list_to_generate(num_questions_to_generate, questions)

        return questions

    @classmethod
    def _prepare_questions_list_to_generate(cls, num_questions_to_generate, questions) -> list:
        shuffle(questions)
        questions = questions[:num_questions_to_generate]

        return questions

    @classmethod
    def _validate_num_questions_to_generate(cls, num_questions_to_generate, questions_to_answers):
        if num_questions_to_generate > len(questions_to_answers):
            raise ValueError("Were asked to generate more questions than those that exist")


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


@dataclass
class MultipleAnswerQuestion(Question):

    _answer_to_explanation: dict

    @property
    def possible_answers(self) -> List[str]:
        return self.answer.split('\n')

    @property
    def answer_to_explanation(self) -> dict:
        return self._answer_to_explanation

    @classmethod
    def generate(cls, questions_to_answers: Dict[str, Dict[str, str]], num_questions_to_generate: int) -> List['MultipleAnswerQuestion']:
        cls._validate_num_questions_to_generate(num_questions_to_generate, questions_to_answers)

        questions = [cls(_answer="\n".join(answers.keys()), _question_str=str(question), _answer_to_explanation=answers)
                     for question, answers in questions_to_answers.items()]

        questions = cls._prepare_questions_list_to_generate(num_questions_to_generate, questions)

        return questions


@dataclass
class MultipleAnswerDisplayableQuestion(DisplayableQuestion, metaclass=ABCMeta):

    _question: MultipleAnswerQuestion
    _already_submitted = []

    def submit_answer(self, answer: str):
        answer = answer.upper()

        if answer in self._question.possible_answers:
            st.write("Correct! :white_check_mark:")
            self._already_submitted.append(answer)

            st.write(self._question.answer_to_explanation[answer])

            left_possible_answers = set(self._question.possible_answers) - set(self._already_submitted)

            if left_possible_answers:
                st.write(f"There are {len(left_possible_answers)} possible answers left")

            else:
                st.write("Congrats! You found all the points we could think about :white_check_mark: :white_check_mark: :white_check_mark:")

        else:
            st.write("The answer you gave is not one of those we regarded :x:")

    def show_answers(self):

        st.write("The possible answers are:")

        for answer, explanation in self._question.answer_to_explanation.items():
            st.write(f"{answer}: {explanation}")
