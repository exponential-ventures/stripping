import os
import unittest

from stripping import setup_stripping_with_catalysis


class TestCacheWithCatalysis(unittest.TestCase):

    def test_has_catalysis_client(self):
        st, _ = setup_stripping_with_catalysis("/tmp/", "local")
        self.assertIsNotNone(st.cache.storage.catalysis_client)

    def test_no_cache_dir_creation(self):
        cache_dir = "/tmp/cache/"
        st, _ = setup_stripping_with_catalysis(cache_dir, "local")
        self.assertFalse(os.path.isdir(cache_dir))
