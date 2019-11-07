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
import os
import shutil

import asynctest

from stripping import setup_stripping
from stripping.cache import StepCache

tmp_dir = os.path.join(os.path.split(__file__)[0], '.test_cache')

st, context = setup_stripping(tmp_dir)


@st.step
def test_step():
    return 'Hello'


class TestCache(asynctest.TestCase):
    def setUp(self):
        self.step_cache = StepCache(tmp_dir)

    def tearDown(self):
        shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_cache_dir_creation(self):
        self.assertTrue(os.path.isdir(tmp_dir))

    async def test_execute_or_retrieve(self):
        self.step_cache.register_context(context)
        step = st.steps[0]
        reponse = await self.step_cache.execute_or_retrieve(step)
        self.assertEqual('Hello', reponse)
