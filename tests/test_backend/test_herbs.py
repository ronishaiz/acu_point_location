from unittest import TestCase


class TestHerbs(TestCase):

    def test_herbs_load(self):
        from backend.herbs.herb import Herb, Flavor, Temperature, TemperatureAccent, HerbGroup, Organ
        from backend.herbs.herb import ALL_HERBS

        self.assertTrue(len(ALL_HERBS) > 0, "No herbs loaded")

        for herb in ALL_HERBS:
            self.assertIsInstance(herb, Herb)
            self.assertIsInstance(herb.name, str)
            self.assertTrue(len(herb.name) > 0, "Herb name is empty")

            if herb.western_name is not None:
                self.assertIsInstance(herb.western_name, str)

            for flavor in herb.flavors:
                self.assertIsInstance(flavor, Flavor)

            if herb.temperature is not None:
                self.assertIsInstance(herb.temperature, Temperature)

            if herb.temperature_accent is not None:
                self.assertIsInstance(herb.temperature_accent, TemperatureAccent)

            if herb.herb_group is not None:
                self.assertIsInstance(herb.herb_group, HerbGroup)

            for organ in herb.affected_organs:
                self.assertIsInstance(organ, Organ)
