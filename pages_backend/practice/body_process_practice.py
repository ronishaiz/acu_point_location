from typing import Optional

from backend.questions.banks.body_process_banks import process_name_to_process
from backend.questions.body_process import BodyProcess, BodyProcessQuestion
from pages_backend.practice.base_practice import BasePractice
from pages_backend.utils import Queue
import streamlit as st
from PIL import Image


class BodyProcessPractice(BasePractice[BodyProcessQuestion]):

    def __init__(self):
        self.process_selection: Optional[BodyProcess] = None

    def set_practice_setting(self):
        self.process_selection = process_name_to_process[st.selectbox(label="Select Process", options=process_name_to_process.keys())]

        image = Image.open(self.process_selection.picture_path)
        st.image(image)

    def get_questions_queue(self) -> Queue[BodyProcessQuestion]:
        questions_to_points = {
            f"Which points are related to pathologies of the {organ.value} in the {self.process_selection.process_name} process?":
                self.process_selection.organ_to_related_points[organ]
            for organ in self.process_selection.organs
        }

        return Queue(BodyProcessQuestion.generate(questions_to_points, len(questions_to_points)))
