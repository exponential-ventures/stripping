import statistics
from datetime import datetime
from numbers import Number

from catalysis.storage import StorageClient


class Elemental:
    formats = [
        'stdout',
        'file',
    ]

    statistics = dict()

    def elemental_report(self, report_name: str,
                         report_type='stdout',
                         path="/tmp/elemental_report.txt",
                         catalysis_client: StorageClient = None) -> None:

        report_type = report_type.lower()

        if report_type not in self.formats:
            raise TypeError(f"Unknown report type. Only allowed: {self.formats}")

        if report_type == 'stdout':

            print(self._generate_report(report_name))

        elif report_type == 'file':

            if catalysis_client is None:
                with open(path, '+w') as f:
                    f.write(self._generate_report(report_name))
            else:
                with catalysis_client.open(path, '+w') as f:
                    f.write(self._generate_report(report_name))

    def _generate_report(self, report_name: str) -> str:
        report = f"\n\n===================== {report_name.upper()} =====================\n"
        report += str(self.statistics) + "\n"
        report += f"===================== GENERATED AT: {datetime.now()} =====================\n"

        return report

    def average(self, l: list):
        self._assert_is_numeric(l)
        return statistics.mean(l)

    @staticmethod
    def _assert_is_numeric(l: list):
        for index, item in enumerate(l):
            if not isinstance(item, Number):
                raise TypeError(f"Item({item}) at index {index} of list is not numeric, is {type(item)}")
