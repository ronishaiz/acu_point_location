from unittest import TestCase

from pages_backend.the_big_picture.the_big_picture import get_big_picture_df


class TestTheBigPicture(TestCase):

    def test_save_big_picture(self):

        df = get_big_picture_df()

        self.assertFalse(df.empty, "big picture df returned empty")
