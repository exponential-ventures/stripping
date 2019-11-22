import asynctest
import pandas as pd

from stripping.elemental.dataset import Dataset

class TestDataset(asynctest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.dt = pd.read_csv('datasets/black_friday.csv', nrows=20)
        cls.dt['Occupation'] = cls.dt['Occupation'].astype(str)
        cls.dt['Purchase'] = cls.dt['Purchase'].astype(int)

    def test_column_selection_with_pandas(self):
        edt = Dataset(self.dt)
        edt.column_selection(['Age', 'Occupation', 'Stay_In_Current_City_Years'])
        self.assertEqual(len(edt.dataFrame.columns), 3)

    def test_filter(self):
        edt = Dataset(self.dt)
        edt.column_selection(['Occupation', 'Purchase'])
        aux = edt.apply_filters([self.avg, self.std])
        self.assertTrue(isinstance(aux, dict))
        average = aux['avg']
        standard_deviation = aux['std']
        self.assertIsNotNone(average)
        self.assertIsNotNone(standard_deviation)
        self.assertTrue(average.Occupation > 0)
        self.assertTrue(average.Purchase > 0)
        self.assertTrue(standard_deviation.Purchase > 0)

    def avg(self, dataframe):
        return dataframe.mean()

    def std(self, dataframe):
        return dataframe.std()