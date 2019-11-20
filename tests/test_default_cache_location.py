from unittest import TestCase

from stripping import setup_stripping


class DefaultCacheLocationTestCase(TestCase):

    def test_default_location_wo_catalysis(self):
        st, _ = setup_stripping()
        self.assertEqual(
            "/usr/src/app/stripping/stripping_cache",
            st.cache.cache_dir,
        )
