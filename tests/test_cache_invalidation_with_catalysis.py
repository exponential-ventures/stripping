from os.path import split, join, exists
import asynctest
import shutil
import asyncio
import tracemalloc
import datetime
import os
from freezegun import freeze_time
from glob import glob

from stripping.cache import StepCache, CacheInvalidation
from stripping import setup_stripping
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
        self.storage.save_step('Pass', 'RETURN_HERE', context)
        await self.cache_invalidation.strategy()
        self.assertTrue(len(glob(f'{tmp_dir}{os.sep}*')) >= 0)

        with freeze_time(datetime.datetime.now() + datetime.timedelta(days=0.25*365)):
            await self.cache_invalidation.strategy()

        self.assertEqual(0, len(glob(f'{tmp_dir}{os.sep}*')))