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


import asynctest
import pandas as pd

from stripping.elemental import Elemental
from stripping.elemental.filters import filters


class TestDataset(asynctest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.dt = pd.read_csv('datasets/black_friday.csv', nrows=30)
        cls.dt['Occupation'] = cls.dt['Occupation'].astype(int)
        cls.dt['Purchase'] = cls.dt['Purchase'].astype(int)
        cls.elemental = Elemental()

    def test_column_selection_and_filters(self):
        self.elemental.column_selection(
            ['Occupation', 'Purchase', 'Age', 'City_Category'])
        self.elemental.report('test elemental')
        self.elemental.filters(*filters)
        self.elemental.analyze(self.dt)
