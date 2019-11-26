#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
## ----------------
## |              |
## | CONFIDENTIAL |
## |              |
## ----------------
##
## Copyright Exponential Ventures LLC (C), 2019 All Rights Reserved
##
## Author: Thales Ribeiro <thales@xnv.io>
## Author: Nathan Martins <nathan@xnv.io>
##
## If you do not have a written authorization to read this code
## PERMANENTLY REMOVE IT FROM YOUR SYSTEM IMMEDIATELY.
##

from datetime import datetime

from catalysis.storage import StorageClient
from pandas.core.frame import DataFrame

STOUT = 'stdout'
FILE = 'file'

FORMATS = [STOUT, FILE]


class Elemental:
    statistics = dict()

    def __init__(self, name: str):
        self.__filters = []
        self._columns = []
        self._path = None
        self._report_type = None
        self._report_name = name
        self._catalysis_client = None

    def column_selection(self, columns: list) -> None:
        self._columns = columns

    def filters(self, *filters):
        self.__filters = filters

    def report(self, path="/tmp/elemental_report.txt", report_type=STOUT, catalysis_client: StorageClient = None):
        self._path = path
        self._report_type = report_type
        self._catalysis_client = catalysis_client
        self._elemental_report()

    def __apply_filters(self, df: DataFrame) -> dict:
        report = {}
        for func in self.__filters:
            report[func.__name__] = func(df)
        return report

    def analyze(self, df: DataFrame):
        df = df[self._columns]
        self._field_inference(df)
        self.statistics = self.__apply_filters(df)

    def _elemental_report(self) -> None:

        if self._report_type not in FORMATS:
            raise TypeError(f"Unknown report type. Only allowed: {FORMATS}")

        if self._report_type == STOUT:

            print(self._generate_report(self._report_name))

        elif self._report_type == FILE:

            if self._catalysis_client is None:
                with open(self._path, '+w') as f:
                    f.write(self._generate_report(self._report_name))
            else:
                with self._catalysis_client.open(self._path, '+w') as f:
                    f.write(self._generate_report(self._report_name))

    def _generate_report(self, report_name: str) -> str:
        report = f"\n\n===================== {report_name} =====================\n"
        for key in self.statistics:
            report += "{} \n".format(key.upper())
            for k in self.statistics[key].keys():
                report += "{} \t {} \n".format(k, self.statistics[key][k])

            report += "\n"

        report += f"===================== GENERATED AT: {datetime.now()} =====================\n"

        return report

    @staticmethod
    def _field_inference(df: DataFrame):
        df.infer_objects()