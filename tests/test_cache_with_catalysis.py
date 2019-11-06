import json
import os
import unittest

from stripping import setup_stripping_with_catalysis


class TestCacheWithCatalysis(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.credentials = json.dumps({
            "local": {
                "driver": "local",
                "path": "/tmp/catalysis/",
            }
        })

    def test_has_catalysis_client(self):
        tmp_dir = os.path.join(os.path.split(__file__)[0], '.test_cache')

        st, _ = setup_stripping_with_catalysis(tmp_dir, self.credentials)

        self.assertIsNotNone(st.cache.storage.catalysis_client)
