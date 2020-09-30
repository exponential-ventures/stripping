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


import shutil
from os.path import split, join

import asynctest

from stripping.executor import Stripping

tmp_dir = join(split(__file__)[0], '.test_cache')


class TestExecutor(asynctest.TestCase):
    def setUp(self):
        self.st = Stripping(tmp_dir)
        self.st.steps = []  # To guarantee no cache from another tests

    def tearDown(self):
        shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_step_decorator(self):
        @self.st.step(skip_cache=False)
        def test_cache():
            pass

        self.assertEqual(1, len(self.st.steps))
        self.assertEqual('test_cache', self.st.steps[0].name)
        self.assertIn('pass\n', self.st.steps[0].code)
