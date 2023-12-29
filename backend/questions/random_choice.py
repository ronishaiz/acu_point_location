import random
from dataclasses import dataclass
from typing import List

from backend.questions.question import DisplayableQuestion, Question

import streamlit as st

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

        for question in questions:
            answer = question.answer
            choices = [answer]

            while answer in choices:
                choices = random.choices(answer_bank, k=NUM_CHOICES - 1)

            choices += [answer]
            random.shuffle(choices)

            random_choice_questions.append(cls(_question=question, _choices=choices))

        return random_choice_questions
