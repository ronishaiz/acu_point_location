import random
from typing import List, Literal, Optional
from dataclasses import dataclass

from backend.herbs.herb import ALL_HERBS, Herb, filter_herbs_by_groups


# Herb groups introduced in commit 672aa6642cd32498395fae78f697426ca8184b18.
SEMESTER_B_HERB_GROUP_VALUES = {
    "ABSORBERS",
    "ANCHORING_SPIRIT_CALMERS",
    "BLEEDING_STOPPERS",
    "BLOOD_MOVERS",
    "BLOOD_TONIFIERS",
    "FOOD_STAGNATION_TREATERS",
    "INTERIOR_HEATERS",
    "QI_MOVERS",
    "QI_TONIFIERS",
    "TONIFYING_SPIRIT_CALMERS",
    "WIND_AND_TREMOR_RELEASERS",
    "YANG_TONIFIERS",
    "YIN_TONIFIERS",
}


@dataclass
class HerbQuestion:
    question: str
    correct_answer: str
    choices: List[str]
    question_type: Literal["herb_group", "focus_remark_to_herb", "herb_to_focus_remark"]


def build_question_key(question: HerbQuestion) -> str:
    return "||".join([
        question.question_type,
        question.question,
        question.correct_answer,
    ])


def _resolve_herb_pool(selected_groups: Optional[List[str]] = None) -> List[Herb]:
    herb_pool = filter_herbs_by_groups(selected_groups) if selected_groups else ALL_HERBS
    if not herb_pool:
        raise ValueError("No herbs found for the selected herb groups")
    return herb_pool


def get_semester_b_herb_group_values() -> List[str]:
    available_group_values = {
        herb.herb_group.value
        for herb in ALL_HERBS
        if herb.herb_group is not None
    }
    return sorted(available_group_values.intersection(SEMESTER_B_HERB_GROUP_VALUES))


def get_semester_a_herb_group_values() -> List[str]:
    available_group_values = {
        herb.herb_group.value
        for herb in ALL_HERBS
        if herb.herb_group is not None
    }
    return sorted(available_group_values.difference(SEMESTER_B_HERB_GROUP_VALUES))


def generate_herb_group_question(herb_pool: List[Herb]) -> HerbQuestion:
    """
    Question: "To which herb group does [herb] belong?"
    Correct answer: the herb group name
    Choices: 4 random herb groups
    """
    herbs_with_group = [herb for herb in herb_pool if herb.herb_group]
    if not herbs_with_group:
        raise ValueError("No grouped herbs found for the selected herb groups")

    herb = random.choice(herbs_with_group)

    correct_answer = herb.herb_group.name.replace('_', ' ').title()

    # Get other herb groups as distractors
    all_groups = set(h.herb_group for h in herbs_with_group if h.herb_group)
    distractors = random.sample(
        [g.name.replace('_', ' ').title() for g in all_groups if g != herb.herb_group],
        min(3, len(all_groups) - 1)
    )

    choices = [correct_answer] + distractors
    random.shuffle(choices)

    return HerbQuestion(
        question=f"To which herb group does **{herb.name}** belong?",
        correct_answer=correct_answer,
        choices=choices,
        question_type="herb_group"
    )


def generate_focus_remark_to_herb_question(herb_pool: List[Herb]) -> HerbQuestion:
    """
    Question: "Which herb has this focus remark: [remark]?"
    Correct answer: the herb name
    Choices: 4 random herbs with different focus remarks
    """
    herbs_with_remarks = [h for h in herb_pool if h.focus_remark]
    if len(herbs_with_remarks) < 2:
        return generate_herb_group_question(herb_pool)  # fallback if not enough herbs

    herb = random.choice(herbs_with_remarks)
    correct_answer = herb.name

    distractors = random.sample(
        [h.name for h in herbs_with_remarks if h.name != herb.name],
        min(3, len(herbs_with_remarks) - 1)
    )

    choices = [correct_answer] + distractors
    random.shuffle(choices)

    return HerbQuestion(
        question=f"Which herb has this focus remark: *{herb.focus_remark}*?",
        correct_answer=correct_answer,
        choices=choices,
        question_type="focus_remark_to_herb"
    )


def generate_herb_to_focus_remark_question(herb_pool: List[Herb]) -> HerbQuestion:
    """
    Question: "What is the focus remark of [herb]?"
    Correct answer: the focus remark
    Choices: 4 random focus remarks
    """
    # Get herbs with focus remarks
    herbs_with_remarks = [h for h in herb_pool if h.focus_remark]
    if len(herbs_with_remarks) < 2:
        return generate_herb_group_question(herb_pool)  # fallback if not enough herbs

    herb = random.choice(herbs_with_remarks)
    correct_answer = herb.focus_remark

    # Get other focus remarks as distractors
    distractors = random.sample(
        [h.focus_remark for h in herbs_with_remarks if h.focus_remark != herb.focus_remark],
        min(3, len(herbs_with_remarks) - 1)
    )

    choices = [correct_answer] + distractors
    random.shuffle(choices)

    return HerbQuestion(
        question=f"What is the focus remark of **{herb.name}**?",
        correct_answer=correct_answer,
        choices=choices,
        question_type="herb_to_focus_remark"
    )


def generate_random_question(
    question_types: Optional[List[str]] = None,
    selected_groups: Optional[List[str]] = None,
) -> HerbQuestion:
    """
    Generate a random herb practice question.
    question_types: list of question types to choose from (default: all types)
    selected_groups: list of herb group enum values to filter the herb pool.
    """
    if not question_types:
        question_types = ["herb_group", "focus_remark_to_herb", "herb_to_focus_remark"]

    herb_pool = _resolve_herb_pool(selected_groups)
    question_type = random.choice(question_types)

    if question_type == "herb_group":
        return generate_herb_group_question(herb_pool)
    elif question_type == "focus_remark_to_herb":
        return generate_focus_remark_to_herb_question(herb_pool)
    else:  # herb_to_focus_remark
        return generate_herb_to_focus_remark_question(herb_pool)


def generate_unique_random_question(
    question_types: Optional[List[str]] = None,
    selected_groups: Optional[List[str]] = None,
    excluded_question_keys: Optional[set[str]] = None,
    max_attempts: int = 120,
) -> HerbQuestion:
    excluded_keys = excluded_question_keys or set()

    for _ in range(max_attempts):
        question = generate_random_question(
            question_types=question_types,
            selected_groups=selected_groups,
        )
        question_key = build_question_key(question)
        if question_key not in excluded_keys:
            return question

    raise ValueError(
        "All available questions for the selected filters and types were already shown in this score cycle. "
        "Use 'Reset Score' to restart the question pool."
    )

