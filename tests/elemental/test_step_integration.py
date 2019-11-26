import unittest
import uuid

import pandas as pd

from stripping.elemental import filters
from stripping.elemental.base import FILE
from tests.utils import set_up_stripping_for_tests


class StepIntegrationCase(unittest.TestCase):

    def test_report_name(self):
        report_name = "test_report"
        report_path = f"/tmp/{str(uuid.uuid4())}-report.txt"

        st, _ = set_up_stripping_for_tests()

        @st.step
        def load_ds():
            return pd.DataFrame()

        st.elemental_step(report_name, path=report_path, report_type=FILE)

        st.execute()

        with open(report_path) as f:
            contents = f.read()
            self.assertIn(report_name, contents)

    def test_initializing_with_last_step_as_input(self):
        st, _ = set_up_stripping_for_tests()

        @st.step
        def load_ds():
            df = pd.read_csv('datasets/black_friday.csv', nrows=20)
            df['Occupation'] = df['Occupation'].astype(int)
            df['Purchase'] = df['Purchase'].astype(int)

            return df

        st.elemental_step("test_report")

        st.execute()

    def test_adding_filters(self):
        st, _ = set_up_stripping_for_tests()
        report_path = f"/tmp/{str(uuid.uuid4())}-report.txt"

        @st.step
        def load_ds():
            df = pd.read_csv('datasets/black_friday.csv', nrows=20)
            df['Occupation'] = df['Occupation'].astype(int)
            df['Purchase'] = df['Purchase'].astype(int)

            return df

        st.elemental_columns(['Occupation', 'Purchase', 'Age', 'City_Category'])
        st.elemental_filters(
            filters.avg,
            filters.min,
            filters.max,
            filters.std,
        )

        st.elemental_step("report name", path=report_path, report_type=FILE)
        st.execute()

        with open(report_path) as f:
            contents = f.read()
            self.assertIn("AVG \nOccupation \t 5.7 \nPurchase \t 13993.8", contents)
            self.assertIn("MIN \nAge \t 0-17 \nCity_Category \t A \nOccupation \t 1 \nPurchase \t 5378", contents)
            self.assertIn("MAX \nAge \t 51-55 \nCity_Category \t C \nOccupation \t 20 \nPurchase \t 19614", contents)
            self.assertIn("STD \nOccupation \t 6.061960773631964 \nPurchase \t 4034.0018605010973", contents)
