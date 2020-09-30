#!/usr/bin/env python3
##
## Authors: Adriano Marques
##          Nathan Martins
##          Thales Ribeiro
##
## Copyright (C) 2019 Exponential Ventures LLC
##
##    This library is free software; you can redistribute it and/or
##    modify it under the terms of the GNU Library General Public
##    License as published by the Free Software Foundation; either
##    version 2 of the License, or (at your option) any later version.
##
##    This library is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
##    Library General Public License for more details.
##
##    You should have received a copy of the GNU Library General Public
##    License along with this library; if not, write to the Free Software
##    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
##


import json
import logging
from datetime import datetime

try:
    from catalysis.storage import StorageClient

    has_catalysis = True
except ImportError as error:
    has_catalysis = False
    logging.warn(f"Not using Catalysis: {str(error)}")
except Exception as error:
    pass

STOUT = 'stdout'
FILE = 'file'
JSON = 'json'

FORMATS = [STOUT, FILE, JSON]


class Elemental:
    statistics = dict()

    def __init__(self):
        self.__filters = []
        self._columns = []
        self._path = None
        self._report_type = None
        self._report_name = None
        self._catalysis_client = None

    def column_selection(self, columns: list) -> None:
        self._columns = columns

    def filters(self, *filters):
        self.__filters = filters

    def report(self, report_name, path="/tmp/elemental_report.txt", report_type=STOUT, catalysis_client=None):
        self._path = path
        self._report_type = report_type
        self._report_name = report_name
        self._catalysis_client = catalysis_client

    def __apply_filters(self, dataframe) -> dict:
        report = {}
        for func in self.__filters:
            report[func.__name__] = func(dataframe)
        return report

    def analyze(self, dataframe):
        dataframe = dataframe[self._columns]
        self._field_infererence(dataframe)
        self.statistics = self.__apply_filters(dataframe)
        self._elemental_report()

    def _elemental_report(self) -> None:

        if self._report_type not in FORMATS:
            raise TypeError(f"Unknown report type. Only allowed: {FORMATS}")

        if self._report_type == STOUT:

            print(self._generate_report(self._report_name))

        elif self._report_type in [FILE, JSON]:

            if self._catalysis_client is None:
                with open(self._path, '+w') as f:
                    if self._report_type == JSON:
                        f.write(self._generate_json_report(self._report_name))
                    else:
                        f.write(self._generate_report(self._report_name))
            elif has_catalysis:
                with self._catalysis_client.open(self._path, '+w') as f:
                    if self._report_type == JSON:
                        f.write(self._generate_json_report(self._report_name))
                    else:
                        f.write(self._generate_report(self._report_name))

    def _generate_report(self, report_name: str) -> str:
        report = f"\n\n===================== {report_name.upper()} =====================\n"
        for key in self.statistics:
            report += "{} \n".format(key.upper())
            for k in self.statistics[key].keys():
                report += "{} \t {} \n".format(k, self.statistics[key][k])

            report += "\n"

        report += f"===================== GENERATED AT: {datetime.now()} =====================\n"

        return report

    def _generate_json_report(self, report_name: str) -> str:
        report = {'name': report_name}
        if self.statistics:
            for key in self.statistics:
                report[key] = {}
                for k in self.statistics[key].keys():
                    report[key][k] = str(self.statistics[key][k])

        report['generated_at'] = str(datetime.now())
        return json.dumps(report)

    @staticmethod
    def _field_infererence(df):
        df.infer_objects()
