#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
## ----------------
## |              |
## | CONFIDENTIAL |
## |              |
## ----------------
##
## Copyright Exponential Ventures LLC (C), 2019 All Rights Reserved
##
## Author: Adriano Marques <adriano@xnv.io>
## Author: Thales Ribeiro  <thales@xnv.io>
##
## If you do not have a written authorization to read this code
## PERMANENTLY REMOVE IT FROM YOUR SYSTEM IMMEDIATELY.
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

ACCESS = 'access'
DIR_PATH = 'path'
logging = logging.getLogger('stripping')


@SingletonDecorator
class StepCache:
    context = None

    def __init__(self, cache_dir: str, catalysis_credential_name: str = ''):
        self.cache_dir = cache_dir
        self.storage = CacheStorage(self.cache_dir, catalysis_credential_name)

        self.cache_invalidation = CacheInvalidation()
        self.cache_invalidation.add_dir(self.cache_dir)

        if '-clean' in sys.argv:
            for item in glob('{}/*'.format(cache_dir)):
                if os.path.isfile(item):
                    os.remove(item)
                else:
                    shutil.rmtree(cache_dir, ignore_errors=True)

        asyncio.ensure_future(self.cache_invalidation.strategy_runner())

    def register_context(self, context):
        self.context = context

    async def execute_or_retrieve(self, step_fn, *args, **kwargs):
        try:
            return self.storage.get_step(step_fn.name, step_fn.code, self.context, *args, **kwargs)
        except StepNotCached:
            logging.info(f"Step '{step_fn.name}' is not cached. Executing...")

            if inspect.iscoroutinefunction(step_fn):
                step_return = await step_fn(*args, **kwargs)
            else:
                step_return = step_fn(*args, **kwargs)

            if not step_fn.skip_cache or not os.environ.get("STRIPPING_SKIP_CACHE", False):
                self.storage.save_step(step_fn.code, step_return, self.context, *args, **kwargs)

            return step_return

    async def execute_or_retrieve_chained_steps(self, chained_steps):

        result = None

        for step in chained_steps:
            if result:
                result = await self.execute_or_retrieve(step, result)
            else:
                result = await self.execute_or_retrieve(step)

        return result


@SingletonDecorator
class CacheInvalidation:

    def __init__(self):
        self.__cached_dirs = {}

    def add_dir(self, cache_dir):
        self.__cached_dirs[cache_dir] = {}

    def force_delete(self, cache_dir):
        logging.info('Attempting to delete {}'.format(cache_dir))

        shutil.rmtree(cache_dir, ignore_errors=True)

        if cache_dir in self.__cached_dirs:
            del (self.__cached_dirs[cache_dir])

        logging.info('<!> {} deleted'.format(cache_dir))

    def strategy(self):
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
                self.__cached_dirs[d][dir_path][ACCESS] = self.__last_access(dir_path)
                if self.__cached_dirs[d][dir_path][ACCESS] <= three_months_ago_timestamp:
                    self.force_delete(dir_path)

            if self.percentage_disk_free_space() < 15.00:
                if len(self.__cached_dirs[d]) > 0:
                    # sort the list by least access
                    sorted_cache_list = sorted(self.__cached_dirs[d].items(), key=lambda x: x[1][ACCESS])
                    self.force_delete(sorted_cache_list[0][0])

    async def strategy_runner(self):
        while True:
            self.strategy()
            await asyncio.sleep(60)

    def __last_access(self, path):
        """
            Returns when the dir was last accessed
        """
        return os.path.getatime(path)

    def year_from_now(self, years: int = 1):
        return datetime.datetime.now() + datetime.timedelta(days=years * 365)

    def year_ago(self, years: float = 1):
        return datetime.datetime.now() - datetime.timedelta(days=years * 365)

    def percentage_disk_free_space(self):
        stats = os.statvfs('/')
        total = stats.f_frsize * stats.f_blocks
        free = stats.f_frsize * stats.f_bavail
        return (free / total) * 100
