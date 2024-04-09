from enum import Enum


class PracticeType(Enum):

    random_choice = "Random Choice Questions"
    point_location = "Point Location"


PRACTICE_TYPES = [PracticeType.random_choice.value, PracticeType.point_location.value]
