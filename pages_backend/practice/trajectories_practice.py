from backend.questions.banks.tajectories_banks import location_to_meridians
from pages_backend.practice.base_practice import BasePractice
from backend.questions.trajectories import TrajectoryQuestion
from pages_backend.utils import Queue


class TrajectoriesPractice(BasePractice[TrajectoryQuestion]):

    def set_practice_setting(self):
        pass

    def get_questions_queue(self) -> Queue[TrajectoryQuestion]:
        location_to_meridian_to_explanation = {}
        for location in location_to_meridians:
            location_to_meridian_to_explanation[location] = {
                meridian.value: explanation for meridian, explanation in location_to_meridians[location].items()}

        questions_to_points = {
            f"Which meridian trajectories path through the {location}?": meridian_to_explanation
            for location, meridian_to_explanation in location_to_meridian_to_explanation.items()
        }

        return Queue(TrajectoryQuestion.generate(questions_to_points, len(questions_to_points)))
