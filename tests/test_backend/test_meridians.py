import unittest

from backend.meridians.meridian import ALL_MERIDIANS


class TestMeridians(unittest.TestCase):

    def test_expected_number_of_learned_points(self):

        for meridian in ALL_MERIDIANS:
            self.assertEqual(meridian.number_of_learned_points, len(meridian.points),
                             f"The meridian: {meridian._organ.value} contains less points than the number of points learned")

    def test_matching_point_identifiers(self):

        for meridian in ALL_MERIDIANS:
            for point in meridian.points:
                self.assertTrue(point.identifier.endswith(str(point.number)), f"The point identifier of {meridian.organ}{point.number} "
                                                                              f"ends with the wrong number. "
                                                                              f"The point identifier is mistakenly: {point.identifier}")
