from unittest import TestCase

from backend.herbs.herb import get_available_herb_groups
from pages_backend.practice.herb_practice import (
    generate_random_question,
    get_semester_a_herb_group_values,
    get_semester_b_herb_group_values,
)


class TestHerbPractice(TestCase):

    def test_semester_a_b_partition_available_groups(self):
        available = {group.value for group in get_available_herb_groups()}
        semester_a = set(get_semester_a_herb_group_values())
        semester_b = set(get_semester_b_herb_group_values())

        self.assertTrue(semester_b, "Semester B groups should not be empty")
        self.assertSetEqual(available, semester_a.union(semester_b))
        self.assertSetEqual(set(), semester_a.intersection(semester_b))

    def test_generate_herb_group_question_honors_group_filter(self):
        selected_group = get_semester_b_herb_group_values()[0]

        question = generate_random_question(
            question_types=["herb_group"],
            selected_groups=[selected_group],
        )

        expected_group_label = selected_group.replace("_", " ").title()
        self.assertEqual(expected_group_label, question.correct_answer)

    def test_generate_random_question_raises_for_empty_filter_result(self):
        with self.assertRaises(ValueError):
            generate_random_question(
                question_types=["herb_group"],
                selected_groups=["GROUP_DOES_NOT_EXIST"],
            )
