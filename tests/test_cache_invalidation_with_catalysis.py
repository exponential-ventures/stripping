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


import datetime
import os
import shutil
import tracemalloc
from glob import glob
from os.path import split, join

import asynctest
from freezegun import freeze_time

from stripping import setup_stripping
from stripping.cache import CacheInvalidation
from stripping.storage import CacheStorage

tmp_dir = join(split(__file__)[0], '.test_cache')

st, context = setup_stripping(tmp_dir)


class TestCacheInvalidationWithCatalysis(asynctest.TestCase):

    @classmethod
    def setUpClass(cls):
        tracemalloc.start()
        cls.storage = CacheStorage(tmp_dir)
        cls.cache_invalidation = CacheInvalidation('local')
        cls.cache_invalidation.add_dir(tmp_dir)

    @classmethod
    def tearDownClass(cls):
        tracemalloc.stop()
        shutil.rmtree(tmp_dir, ignore_errors=True)

    async def test_strategy(self):
        self.storage.save_step('Pass', 'step_name', 'RETURN_HERE', context)
        await self.cache_invalidation.strategy()
        self.assertTrue(len(glob(f'{tmp_dir}{os.sep}*')) >= 0)

        with freeze_time(datetime.datetime.now() + datetime.timedelta(days=0.25 * 365)):
            await self.cache_invalidation.strategy()

        self.assertEqual(0, len(glob(f'{tmp_dir}{os.sep}*')))
