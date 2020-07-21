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


import os
import shutil
import uuid

import asynctest

from stripping import setup_stripping
from stripping.cache import StepCache

tmp_dir = f"/tmp/{str(uuid.uuid4())}/cache/"

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
