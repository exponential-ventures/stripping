import unittest

import pandas as pd

from stripping.elemental.base import FILE
from tests.utils import set_up_stripping_for_tests


class StepIntegrationCase(unittest.TestCase):

    def test_report_name(self):
        report_name = "test_report"
        report_path = "/tmp/report.txt"

        st, _ = set_up_stripping_for_tests()

        @st.step
        def load_ds():
            return pd.DataFrame()

        st.elemental_step(report_name, path=report_path, report_type=FILE)
        self.assertIsNotNone(st.elemental)

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

        self.assertIsNotNone(st.elemental)
