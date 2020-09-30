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

from stripping.exceptions import StepNotCached
from stripping.executor import Context
from stripping.storage import CacheStorage

tmp_dir = join(split(__file__)[0], '.test_cache')
context = Context()


class TestStorage(asynctest.TestCase):
    def setUp(self):
        self.storage = CacheStorage(tmp_dir)

    def tearDown(self):
        shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_save_step(self):
        self.storage.save_step('Pass', 'RETURN_HERE', context)
        aux = self.storage.get_step('', 'Pass', context)
        self.assertEqual(aux, 'RETURN_HERE')  # That means the code/step was found
        with self.assertRaises(StepNotCached):
            self.storage.get_step('', 'PHONY_CODE', context)

    def test_step_location(self):
        aux = self.storage.step_location('Pass')
        # The len(aux) should be 3 because it means
        # location, return location and context location path
        self.assertEqual(3, len(aux))
