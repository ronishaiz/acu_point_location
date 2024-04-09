from backend.questions.banks.point_location_question_banks import AREAS, EXISTING_MERIDIANS, BY_AREA, BY_MERIDIAN
from backend.questions.point_location import PointLocation
from pages_backend.practice.base_practice import BasePractice
from pages_backend.utils import Queue

import streamlit as st


class PointLocationPractice(BasePractice[PointLocation]):

    def __init__(self):
        self.areas_selection = None
        self.meridian_selection = None

    def set_practice_setting(self):
        self.areas_selection = st.multiselect("Select Body Areas", AREAS, default=AREAS, on_change=self.regenerate)
        self.meridian_selection = st.multiselect("Select Meridians", EXISTING_MERIDIANS, default=EXISTING_MERIDIANS, on_change=self.regenerate)

    def get_questions_queue(self) -> Queue[PointLocation]:
        question_to_answer = self._create_question_to_answer_dict()
        questions = PointLocation.generate(question_to_answer, len(question_to_answer))

        return Queue[PointLocation](questions)

    def _create_question_to_answer_dict(self) -> dict:
        relevant_by_area = {area: points for area, points in BY_AREA.items() if area in self.areas_selection}
        all_area_points = [point for points_list in relevant_by_area.values() for point in points_list]

        relevant_by_meridian = {meridian: points for meridian, points in BY_MERIDIAN.items() if meridian in self.meridian_selection}
        all_meridian_points = [point for points_list in relevant_by_meridian.values() for point in points_list]

        all_points = set(all_area_points).intersection(set(all_meridian_points))

        return {point: point for point in all_points}
