from unittest import TestCase

from stripping import setup_stripping, setup_stripping_with_catalysis


class DefaultCacheLocationTestCase(TestCase):

    def test_default_location_wo_catalysis(self):
        st, _ = setup_stripping()
        self.assertEqual(
            "/usr/src/app/stripping/stripping_cache",
            st.cache.cache_dir,
        )

    def test_default_location_with_catalysis(self):
        st, _ = setup_stripping_with_catalysis(catalysis_credential_name="local")
        self.assertEqual(
            "/tmp/list/",
            st.cache.cache_dir,
        )
