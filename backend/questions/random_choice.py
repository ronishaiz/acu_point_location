import random
from dataclasses import dataclass
from typing import List

from backend.questions.question import DisplayableQuestion, Question

import streamlit as st

from pages_backend.utils import format_displayable_object

NUM_CHOICES = 4


@dataclass
class RandomChoice(DisplayableQuestion):

    _choices: list

    def display(self):
        answer = st.radio(label=str(self._question.question_str), options=self._choices)

        st.button("Submit", key="Submit Answer", on_click=lambda: self.submit_answer(answer))

    @classmethod
    def generate(cls, questions_to_answers: dict, num_questions_to_generate: int) -> List['RandomChoice']:

        questions = Question.generate(questions_to_answers, num_questions_to_generate)

        random_choice_questions = []
        answer_bank = list(questions_to_answers.values())
        answer_bank = set(cls._reformat_answer_bank(answer_bank))

        for question in questions:
            answer = question.answer

            choices = [str(answer)]
            for _ in range(NUM_CHOICES - 1):
                choices.append(random.choice(list(answer_bank - set(choices))))

            random.shuffle(choices)

            random_choice_questions.append(cls(_question=question, _choices=choices))

        return random_choice_questions

    @classmethod
    def _reformat_answer_bank(cls, answers: list) -> list:
        new_answers = []

        for answer in answers:
            answer = format_displayable_object(answer)

            if str(answer) not in new_answers:
                new_answers.append(str(answer))

        return new_answers
