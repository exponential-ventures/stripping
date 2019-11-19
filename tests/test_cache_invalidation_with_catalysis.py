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
from catalysis.common.pool_manager import PoolManager

tmp_dir = join(split(__file__)[0], '.test_cache')

st, context = setup_stripping(tmp_dir)

pool_manager = PoolManager(max_connections=5, known_proxies=[])


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

    def test_strategy(self):
        asyncio.get_event_loop().run_until_complete(pool_manager.create_connection('wss://0.0.0.0:6745'))
        self.storage.save_step('Pass', 'RETURN_HERE', context)
        self.cache_invalidation.strategy()
        self.assertTrue(len(glob(f'{tmp_dir}{os.sep}*')) >= 0)

        with freeze_time(datetime.datetime.now() + datetime.timedelta(days=0.25*365)):
            self.cache_invalidation.strategy()

        self.assertEqual(0, len(glob(f'{tmp_dir}{os.sep}*')))
