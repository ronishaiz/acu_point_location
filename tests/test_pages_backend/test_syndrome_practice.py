from unittest import TestCase

from pages_backend.practice.syndrome_practice import (
    _jaccard_similarity,
    filter_syndromes_by_organs,
    generate_random_question,
    get_syndrome_organ_options,
)


class TestSyndromePractice(TestCase):

    def test_get_syndrome_organ_options_has_values(self):
        options = get_syndrome_organ_options()

        self.assertTrue(options)
        self.assertTrue(all("value" in option and "label" in option for option in options))

    def test_filter_syndromes_by_organs(self):
        options = get_syndrome_organ_options()
        selected_organ = options[0]["value"]

        filtered = filter_syndromes_by_organs([selected_organ])

        self.assertTrue(filtered)
        self.assertTrue(all(syndrome.organ.value == selected_organ for syndrome in filtered))

    def test_generate_random_question_selected_type(self):
        question = generate_random_question(
            question_types=["syndrome_to_treatment_principle"],
            selected_organs=["LIV"],
        )

        self.assertEqual("syndrome_to_treatment_principle", question.question_type)
        self.assertIn(question.correct_answer, question.choices)

    def test_generate_random_question_raises_for_empty_filter_result(self):
        with self.assertRaises(ValueError):
            generate_random_question(
                question_types=["pulse_to_syndrome"],
                selected_organs=["PC"],
            )

    def test_jaccard_similarity(self):
        score = _jaccard_similarity({"a", "b"}, {"b", "c"})
        self.assertEqual(1 / 3, score)
