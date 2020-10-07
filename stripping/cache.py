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


import asyncio
import datetime
import inspect
import logging
import os
import shutil
import sys
from glob import glob

from .exceptions import StepNotCached
from .singleton import SingletonDecorator
from .storage import CacheStorage

try:
    from catalysis.storage.storage_client import StorageClient

    has_catalysis = True
except ImportError as error:
    has_catalysis = False
    logging.warn(f"Not using Catalysis: {str(error)}")
except Exception as error:
    pass

ACCESS = 'access'
DIR_PATH = 'path'
logging = logging.getLogger('stripping')


@SingletonDecorator
class StepCache:
    context = None

    def __init__(self, cache_dir: str, catalysis_credential_name: str = ''):
        self.cache_dir = cache_dir
        self.storage = CacheStorage(self.cache_dir, catalysis_credential_name)

        self.cache_invalidation = CacheInvalidation(catalysis_credential_name)
        self.cache_invalidation.add_dir(self.cache_dir)

        if '-clean' in sys.argv:
            for item in glob('{}/*'.format(cache_dir)):
                if os.path.isfile(item):
                    os.remove(item)
                else:
                    shutil.rmtree(cache_dir, ignore_errors=True)

        # asyncio.ensure_future(self.cache_invalidation.strategy_runner())

    def register_context(self, context):
        self.context = context

    async def execute_or_retrieve(self, step_fn, *args, **kwargs):

        if step_fn.skip_cache or os.environ.get("STRIPPING_SKIP_CACHE", False):
            logging.info(f"Step '{step_fn.name}' has skip_cache=True. Executing...")

            if inspect.iscoroutinefunction(step_fn):
                step_return = await step_fn(*args, **kwargs)
            else:
                step_return = step_fn(*args, **kwargs)

            return step_return

        try:
            return self.storage.get_step(step_fn, self.context, *args, **kwargs)
        except StepNotCached:
            logging.info(f"Step '{step_fn.name}' is not cached. Executing...")

            if inspect.iscoroutinefunction(step_fn):
                step_return = await step_fn(*args, **kwargs)
            else:
                step_return = step_fn(*args, **kwargs)

            self.storage.save_step(step_fn, step_return, self.context, *args, **kwargs)

            return step_return


@SingletonDecorator
class CacheInvalidation:

    def __init__(self, catalysis_credential_name: str = ''):
        self.__cached_dirs = {}
        self.catalysis_client = None

        if has_catalysis and catalysis_credential_name != '':
            self.catalysis_client = StorageClient(catalysis_credential_name)

    def add_dir(self, cache_dir):
        self.__cached_dirs[cache_dir] = {}

    async def force_delete(self, cache_dir):
        logging.info('Attempting to delete {}'.format(cache_dir))

        if self.catalysis_client:
            with self.catalysis_client.open(cache_dir) as remote:
                await remote.delete()
                logging.info('<!> {} deleted'.format(cache_dir))
        else:
            shutil.rmtree(cache_dir, ignore_errors=True)
            logging.info('<!> {} deleted'.format(cache_dir))

        if cache_dir in self.__cached_dirs:
            del (self.__cached_dirs[cache_dir])

    async def strategy(self):
        """
            A Cache is deleted when:
                - it haven't being accessed for 4 months or more.
                - free disk space reaches <= 15%
        """

        three_months_ago_timestamp = datetime.datetime.timestamp(self.year_ago(0.25))

        for d in self.__cached_dirs.keys():
            self.__cached_dirs[d] = {}
            for dir_path in glob('{}/*'.format(d)):
                self.__cached_dirs[d][dir_path] = {}
                self.__cached_dirs[d][dir_path][ACCESS] = await self.__last_access( dir_path)
                if self.__cached_dirs[d][dir_path][ACCESS] <= three_months_ago_timestamp:
                    await self.force_delete(dir_path)
                await asyncio.sleep(0.2)

            if await self.percentage_disk_free_space() < 15.00:
                if len(self.__cached_dirs[d]) > 0:
                    # sort the list by least access
                    sorted_cache_list = sorted(self.__cached_dirs[d].items(), key=lambda x: x[1][ACCESS])
                    await self.force_delete(sorted_cache_list[0][0])

    async def strategy_runner(self):
        while True:
            await self.strategy()
            await asyncio.sleep(60)

    async def __last_access(self, path):
        """
            Returns when the dir was last accessed
        """
        if self.catalysis_client:
            with self.catalysis_client.open(path) as remote:
                return await remote.getatime()
        else:
            return os.path.getatime(path)

    def year_from_now(self, years: int = 1):
        return datetime.datetime.now() + datetime.timedelta(days=years * 365)

    def year_ago(self, years: float = 1):
        return datetime.datetime.now() - datetime.timedelta(days=years * 365)

    async def percentage_disk_free_space(self):
        if self.catalysis_client:
            with self.catalysis_client.open('/') as remote:
                return await remote.free_space()
        else:
            stats = os.statvfs('/')
            total = stats.f_frsize * stats.f_blocks
            free = stats.f_frsize * stats.f_bavail
            return (free / total) * 100

