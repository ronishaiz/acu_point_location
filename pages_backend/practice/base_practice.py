from abc import abstractmethod
from typing import TypeVar, Generic

import streamlit as st

from backend.questions.question import DisplayableQuestion
from pages_backend.utils import Queue

QUESTION_T = TypeVar('QUESTION_T', bound=DisplayableQuestion)


class BasePractice(Generic[QUESTION_T]):

    _PRACTICE_STATE_KEY = "practice_state"

    def practice(self):
        self.set_practice_setting()

        if self._PRACTICE_STATE_KEY not in st.session_state:
            st.session_state[self._PRACTICE_STATE_KEY] = self.get_questions_queue()

        self.show_questions()

    @abstractmethod
    def set_practice_setting(self):
        pass

    @abstractmethod
    def get_questions_queue(self) -> Queue[QUESTION_T]:
        pass

    @classmethod
    def regenerate(cls):
        if cls._PRACTICE_STATE_KEY in st.session_state:
            st.session_state.pop(cls._PRACTICE_STATE_KEY)

    @classmethod
    def next(cls, questions_q: Queue[QUESTION_T]):
        questions_q.get_top().reset()
        questions_q.next()

    @classmethod
    def prev(cls, questions_q: Queue[QUESTION_T]):
        questions_q.get_top().reset()
        questions_q.prev()

    @classmethod
    def show_questions(cls):
        q = st.session_state[cls._PRACTICE_STATE_KEY]

        if not q.empty:
            q.get_top().display()

            st.button("Previous", on_click=cls.prev, kwargs={"questions_q": q}, key="previous_question")
            st.button("Next", on_click=cls.next, kwargs={"questions_q": q}, key="next_question")
