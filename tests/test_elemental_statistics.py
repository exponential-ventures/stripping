import unittest

from stripping.elemental import Elemental


class ElementalStatisticsTestCase(unittest.TestCase):
    def test_average(self):
        l = [
            2, 3.0, 3, 5, 5, 7, 10
        ]

        e = Elemental()
        self.assertEqual(e.average(l), 5)

    def test_average_non_numeric(self):
        l = [
            2, 3.0, "potato", 5, 5, 7, 10
        ]

        e = Elemental()
        with self.assertRaises(TypeError):
            e.average(l)
