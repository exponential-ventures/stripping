import asynctest
import pandas as pd

from stripping.elemental import Elemental
from stripping.elemental.filters import (avg, std, max, min, count, count_null, count_notnull, max_length, min_length,
                                         avg_length, number_uniques, memory_size, memory_avg)


class TestDataset(asynctest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.dt = pd.read_csv('datasets/black_friday.csv', nrows=20)
        cls.dt['Occupation'] = cls.dt['Occupation'].astype(int)
        cls.dt['Purchase'] = cls.dt['Purchase'].astype(int)
        cls.elemental = Elemental()

    def test_column_selection_and_filters(self):
        self.elemental.column_selection(
            ['Occupation', 'Purchase', 'Age', 'City_Category'])
        self.elemental.report('test elemental')
        self.elemental.filters(avg, std, max, min, count,
                               count_null, count_notnull, max_length, min_length, avg_length, number_uniques,
                               memory_size, memory_avg)
        self.elemental.analyze(self.dt)
