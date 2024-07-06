import os.path
import unittest

from backend.enums import MeridianName
from backend.meridians.meridian_trajectory import MeridianTrajectory
from backend import meridians


class TestMeridianTrajectory(unittest.TestCase):

    def setUp(self):
        self.trajectories_folder = os.path.join(os.path.dirname(meridians.__file__), 'data', 'trajectories')
        self.descriptions_folder = os.path.join(self.trajectories_folder, 'descriptions')

    def test_from_toml(self):
        # Prepare
        path_1_str_rep = ('Outer Path 2:\nAnterior part of the arm -> Anterior-radial part of the forearm -> Styloid of Radius -> '
                          'The root of the palm -> The radial side of the first metacarpal -> Ends in the radial part of the thumbnail')

        # Act
        lu_traj = MeridianTrajectory.from_toml(MeridianName.LU)

        # Assert
        self.assertEqual(3, len(lu_traj.paths), "unexpected number of paths")
        self.assertEqual(path_1_str_rep, lu_traj.paths[1].str_rep, "unexpected string representation for path 1")
        self.assertFalse(lu_traj.paths[1].inner, "path 1 should be outer")

    def test_indices(self):

        # Act
        for description in os.listdir(self.descriptions_folder):
            traj = MeridianTrajectory.from_toml(MeridianName(description.replace('.toml', '')))
            indices = [path.index for path in traj.paths]

            # Assert
            self.assertListEqual(list(range(1, len(indices) + 1)), indices, "the indices of the paths must be monotonic and rising")

    def test_descriptions_and_pictures_match(self):

        # Act
        for description in os.listdir(self.descriptions_folder):
            image_path = os.path.join(self.trajectories_folder, 'images', description.replace('.toml', '.png'))

            # Assert
            self.assertTrue(os.path.exists(image_path), "the expected image path does not exist")
