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
##
## If you do not have a written authorization to read this code
## PERMANENTLY REMOVE IT FROM YOUR SYSTEM IMMEDIATELY.
##

from pandas.core.frame import DataFrame

class Dataset:
    def __init__(self, dataframe: DataFrame):
        self.dataFrame = dataframe

    def column_selection(self, columns: list) -> None:
        self.dataFrame = self.dataFrame[columns]

    def apply_filters(self, filters) -> dict:
        report = {}
        for func in filters:
            report[func.__name__] = func(self.dataFrame)
        return report

