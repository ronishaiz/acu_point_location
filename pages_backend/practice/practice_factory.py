from pages_backend.practice.base_practice import BasePractice
from pages_backend.practice.body_process_practice import BodyProcessPractice
from pages_backend.practice.point_location_practice import PointLocationPractice
from pages_backend.practice.practice_type import PracticeType
from pages_backend.practice.random_choice_practice import RandomChoicePractice


def get_practice(practice_str: str) -> BasePractice:
    if practice_str == PracticeType.random_choice.value:
        return RandomChoicePractice()

    elif practice_str == PracticeType.point_location.value:
        return PointLocationPractice()

    elif practice_str == PracticeType.body_process_pathologies.value:
        return BodyProcessPractice()

    else:
        raise ValueError(f"The provided practice_str: {practice_str} is currently unsupported")
