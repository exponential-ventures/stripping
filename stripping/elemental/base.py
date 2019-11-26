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

    def __init__(self, name: str, ds: DataFrame):
        self.__filters = []
        self._columns = []
        self._path = None
        self._report_type = None
        self._report_name = name
        self.ds = ds
        self._catalysis_client = None

    def column_selection(self, columns: list) -> None:
        self._columns = columns

    def filters(self, *filters):
        self.__filters = filters

    def report(self, name: str, path="/tmp/elemental_report.txt", report_type=STOUT,
               catalysis_client: StorageClient = None):

        if report_type not in FORMATS:
            raise TypeError(f"Unknown report type. Only allowed: {FORMATS}")

        if report_type == STOUT:
            print(self._generate_report(name))

        elif report_type == FILE:

            if catalysis_client is None:
                with open(path, '+w') as f:
                    f.write(self._generate_report(name))
            else:
                with catalysis_client.open(self._path, '+w') as f:
                    f.write(self._generate_report(name))

    def analyze(self):
        df = self.ds[self._columns]

        self._field_inference(df)

        self.statistics = self.__apply_filters(df)

    def __apply_filters(self, df: DataFrame) -> dict:
        report = {}
        for func in self.__filters:
            report[func.__name__] = func(df)
        return report

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
