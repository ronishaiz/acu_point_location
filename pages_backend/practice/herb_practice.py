import random
from typing import List, Literal
from dataclasses import dataclass

from backend.herbs.herb import ALL_HERBS


@dataclass
class HerbQuestion:
    question: str
    correct_answer: str
    choices: List[str]
    question_type: Literal["herb_group", "focus_remark_to_herb", "herb_to_focus_remark"]


def generate_herb_group_question() -> HerbQuestion:
    """
    Question: "To which herb group does [herb] belong?"
    Correct answer: the herb group name
    Choices: 4 random herb groups
    """
    herb = random.choice(ALL_HERBS)
    if not herb.herb_group:
        return generate_herb_group_question()  # retry if herb has no group

    correct_answer = herb.herb_group.name.replace('_', ' ').title()

    # Get other herb groups as distractors
    all_groups = set(h.herb_group for h in ALL_HERBS if h.herb_group)
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


def generate_focus_remark_to_herb_question() -> HerbQuestion:
    """
    Question: "Which herb has this focus remark: [remark]?"
    Correct answer: the herb name
    Choices: 4 random herbs with different focus remarks
    """
    # Get herbs with focus remarks
    herbs_with_remarks = [h for h in ALL_HERBS if h.focus_remark]
    if len(herbs_with_remarks) < 2:
        return generate_herb_group_question()  # fallback if not enough herbs

    herb = random.choice(herbs_with_remarks)
    correct_answer = herb.name

    # Get other herbs as distractors
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


def generate_herb_to_focus_remark_question() -> HerbQuestion:
    """
    Question: "What is the focus remark of [herb]?"
    Correct answer: the focus remark
    Choices: 4 random focus remarks
    """
    # Get herbs with focus remarks
    herbs_with_remarks = [h for h in ALL_HERBS if h.focus_remark]
    if len(herbs_with_remarks) < 2:
        return generate_herb_group_question()  # fallback if not enough herbs

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


def generate_random_question(question_types: List[str] = None) -> HerbQuestion:
    """
    Generate a random herb practice question.
    question_types: list of question types to choose from (default: all types)
    """
    if not question_types:
        question_types = ["herb_group", "focus_remark_to_herb", "herb_to_focus_remark"]

    question_type = random.choice(question_types)

    if question_type == "herb_group":
        return generate_herb_group_question()
    elif question_type == "focus_remark_to_herb":
        return generate_focus_remark_to_herb_question()
    else:  # herb_to_focus_remark
        return generate_herb_to_focus_remark_question()

