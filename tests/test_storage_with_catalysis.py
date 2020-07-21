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
import uuid

import asynctest

from stripping import setup_stripping_with_catalysis


class TestStorageWithCatalysis(asynctest.TestCase):

    def test_has_catalysis_client(self):
        st, _ = setup_stripping_with_catalysis("/tmp/", "local")
        self.assertIsNotNone(st.cache.storage.catalysis_client)

    def test_no_cache_dir_creation(self):
        random = str(uuid.uuid4())

        cache_dir = f"/tmp/{random}/cache/"
        st, _ = setup_stripping_with_catalysis(cache_dir, "local")
        self.assertFalse(os.path.isdir(cache_dir))

    async def test_save_step_remotely(self):
        random = str(uuid.uuid4())

        cache_dir = f"/tmp/{random}/cache/"

        stripping, context = setup_stripping_with_catalysis(cache_dir, "local")

        storage = stripping.cache.storage
        storage.save_step('Pass', 'RETURN_HERE', context)

    async def test_get_step_remotely(self):
        random = str(uuid.uuid4())

        cache_dir = f"/tmp/{random}/cache/"

        stripping, context = setup_stripping_with_catalysis(cache_dir, "local")

        storage = stripping.cache.storage
        storage.save_step('Pass', 'RETURN_HERE', context)

        aux = storage.step_location('Pass')
        # The len(aux) should be 3 because it means
        # location, return location and context location path
        self.assertEqual(3, len(aux))
