import asynctest
import pandas as pd

from stripping.elemental import Elemental, filters


class TestDataset(asynctest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.dt = pd.read_csv('datasets/black_friday.csv', nrows=20)
        cls.dt['Occupation'] = cls.dt['Occupation'].astype(int)
        cls.dt['Purchase'] = cls.dt['Purchase'].astype(int)
        cls.elemental = Elemental('test elemental')

    def test_column_selection_and_filters(self):

        self.elemental.column_selection(['Occupation', 'Purchase', 'Age', 'City_Category'])

        self.elemental.filters(
            filters.avg,
            filters.std,
            filters.max,
            filters.min,
            filters.count,
            filters.count_null,
            filters.count_notnull,
            filters.max_length,
            filters.min_length,
            filters.avg_length,
            filters.number_uniques,
            filters.memory_size,
            filters.memory_avg,
        )

        self.elemental.analyze(self.dt)
        self.elemental.report()
