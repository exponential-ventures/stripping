import asynctest
import shutil
import tracemalloc
import datetime
import os
from os.path import split, join, exists
from freezegun import freeze_time
from glob import glob

from stripping.cache import StepCache, CacheInvalidation
from stripping import setup_stripping
from stripping.storage import CacheStorage

tmp_dir = join(split(__file__)[0], '.test_cache')

st, context = setup_stripping(tmp_dir)


class TestCacheInvalidation(asynctest.TestCase):

    def setUp(self):
        tracemalloc.start()
        self.storage = CacheStorage(tmp_dir)
        self.cache_invalidation = CacheInvalidation()
        self.cache_invalidation.add_dir(tmp_dir)

    def tearDown(self):
        tracemalloc.stop()
        shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_strategy(self):
        self.storage.save_step('Pass', 'RETURN_HERE', context)
        self.cache_invalidation.strategy()
        self.assertTrue(len(glob(f'{tmp_dir}{os.sep}*')) >= 0)

        with freeze_time(datetime.datetime.now() + datetime.timedelta(days=1*365)):
            self.cache_invalidation.strategy()

        self.assertEqual(0, len(glob(f'{tmp_dir}{os.sep}*')))







