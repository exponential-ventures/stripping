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
