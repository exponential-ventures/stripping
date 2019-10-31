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

import asynctest
import shutil
from os.path import split, join

from stripping.storage import CacheStorage
from stripping.executor import Context
from stripping.exceptions import StepNotCached

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
        self.assertEqual(aux, 'RETURN_HERE') # That means the code/step was found
        with self.assertRaises(StepNotCached):
            self.storage.get_step('', 'PHONY_CODE', context)


    def test_step_location(self):
       aux = self.storage.step_location('Pass')
       # The len(aux) should be 3 because it means
       # location, return location and context location path
       self.assertEqual(3, len(aux))

