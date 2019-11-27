import asynctest
import pandas as pd

from stripping.elemental import Elemental
from stripping.elemental.filters import filters


class TestDataset(asynctest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.dt = pd.read_csv('datasets/black_friday.csv', nrows=30)
        cls.dt['Occupation'] = cls.dt['Occupation'].astype(int)
        cls.dt['Purchase'] = cls.dt['Purchase'].astype(int)
        cls.elemental = Elemental()

    def test_column_selection_and_filters(self):
        self.elemental.column_selection(
            ['Occupation', 'Purchase', 'Age', 'City_Category'])
        self.elemental.report('test elemental')
        self.elemental.filters(*filters)
        self.elemental.analyze(self.dt)
