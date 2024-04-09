import unittest

from pages_backend.practice.point_location_practice import PointLocationPractice


class TestPointLocationPractice(unittest.TestCase):

    def test_create_question_to_answer_dict(self):
        # Prepare
        practice = PointLocationPractice()
        practice.areas_selection = ["chest and abdomen", "leg"]
        practice.meridian_selection = ["ST", "CV"]

        expected_result = {'CV2': 'CV2', 'CV14': 'CV14', 'CV6': 'CV6', 'CV9': 'CV9', 'CV3': 'CV3', 'CV17': 'CV17', 'ST30': 'ST30', 'ST21': 'ST21',
                           'ST39': 'ST39', 'CV16': 'CV16', 'ST28': 'ST28', 'ST18': 'ST18', 'ST12': 'ST12', 'ST36': 'ST36', 'CV22': 'CV22',
                           'ST34': 'ST34', 'ST38': 'ST38', 'ST25': 'ST25', 'ST40': 'ST40', 'ST35': 'ST35', 'CV12': 'CV12', 'ST37': 'ST37',
                           'CV8': 'CV8', 'ST31': 'ST31', 'CV7': 'CV7', 'ST17': 'ST17', 'CV15': 'CV15', 'CV4': 'CV4', 'CV5': 'CV5'}

        # Act
        question_to_answer = practice._create_question_to_answer_dict()

        # Assert
        self.assertDictEqual(expected_result, question_to_answer)
