import asynctest
import pandas as pd

from stripping.elemental import Elemental


class TestDataset(asynctest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.dt = pd.read_csv('datasets/black_friday.csv', nrows=20)
        cls.dt['Occupation'] = cls.dt['Occupation'].astype(int)
        cls.dt['Purchase'] = cls.dt['Purchase'].astype(int)
        cls.elemental = Elemental()

    def test_column_selection_and_filters(self):
        self.elemental.column_selection(['Occupation', 'Purchase'])
        self.elemental.report('test elemental')
        self.elemental.filters(self.avg, self.std)
        self.elemental.analyze(self.dt)

    def avg(self, dataframe):
        return dataframe.mean()

    def std(self, dataframe):
        return dataframe.std()
