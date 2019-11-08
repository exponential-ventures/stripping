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
        @self.st.step
        def test_cache():
            pass

        self.assertEqual(1, len(self.st.steps))
        self.assertEqual('test_cache', self.st.steps[0].name)
        self.assertIn('pass\n', self.st.steps[0].code)
