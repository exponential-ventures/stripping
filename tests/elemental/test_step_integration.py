import unittest

from stripping import setup_stripping
from stripping.elemental.base import FILE


class StepIntegrationCase(unittest.TestCase):

    def test_report_name(self):
        name = "test_report"

        st, _ = setup_stripping("/tmp/")
        st.elemental_step(name)
        self.assertIsNotNone(st.elemental)

        report_path = "/tmp/report.txt"

        st.elemental.report(path=report_path, report_type=FILE)

        with open(report_path) as f:
            contents = f.read()
            self.assertIn(name, contents)
