import unittest

from backend.meridians.meridian import ALL_MERIDIANS, get_point_by_identifier
from backend.points.point import Point


class TestMeridians(unittest.TestCase):

    def test_expected_number_of_learned_points(self):

        for meridian in ALL_MERIDIANS:
            self.assertEqual(meridian.number_of_learned_points, len(meridian.points),
                             f"The meridian: {meridian._name.value} contains less points than the number of points learned")

    def test_matching_point_identifiers(self):

        for meridian in ALL_MERIDIANS:
            for point in meridian.points:
                self.assertTrue(point.identifier.endswith(str(point.number)), f"The point identifier of {meridian.name}{point.number} "
                                                                              f"ends with the wrong number. "
                                                                              f"The point identifier is mistakenly: {point.identifier}")

    def test_get_point_by_identifier(self):

        point = get_point_by_identifier('SP15')

        expected_point = Point(
            _identifier='SP15', _chinese_name='Da Heng', _number=15, _characters=[],
            _location='4 cun lateral to the umbilicus, at the lateral border of the Rectus Abdominus muscle (at the height of CV8 and ST25)',
            _functions=['Harmonizes the intestines'],
            _indications=['LI Damp Heat', 'Soft Stool', 'Pencil-like Stool', 'Going to the toilets many times',
                          'Constipation (based on SP Qi Xu)'])

        self.assertEqual(expected_point, point)

    def test_get_non_existing_point_by_identifier(self):

        with self.assertRaises(ValueError, msg="Could not find the point with the identifier: SP18 in the meridian: SP"):
            get_point_by_identifier('SP18')
