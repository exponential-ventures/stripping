import unittest

from stripping import setup_stripping_with_catalysis


class TestCacheWithCatalysis(unittest.TestCase):

    def test_has_catalysis_client(self):
        st, _ = setup_stripping_with_catalysis("/tmp/", "local")
        self.assertIsNotNone(st.cache.storage.catalysis_client)
