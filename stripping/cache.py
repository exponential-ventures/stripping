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
import inspect
from glob import glob
import os
import datetime
import logging

from .exceptions import StepNotCached
from .singleton import SingletonDecorator
from .storage import CacheStorage

ACCESS = 'acess'
DIR_PATH = 'path'
LOG = logging.getLogger('stripping')


@SingletonDecorator
class StepCache:
    context = None

    def __init__(self, cache_dir):
        self.cache_dir = cache_dir
        self.storage = CacheStorage(self.cache_dir)

        self.cache_invalidation = CacheInvalidation()
        self.cache_invalidation.add_dir(self.cache_dir)
        asyncio.ensure_future(self.cache_invalidation.strategy_runner())

    def register_context(self, context):
        self.context = context

    async def execute_or_retrieve(self, step_fn, *args, **kwargs):
        try:
            return self.storage.get_step(step_fn.name, step_fn.code, self.context, *args, **kwargs)
        except StepNotCached:
            LOG.info(f"Step '{step_fn.name}' is not cached. Executing...")
            step_return = None

            if inspect.iscoroutinefunction(step_fn):
                step_return = await step_fn(*args, **kwargs)
            else:
                step_return = step_fn(*args, **kwargs)

            self.storage.save_step(
                step_fn.code, step_return, self.context, *args, **kwargs)

            return step_return


@SingletonDecorator
class CacheInvalidation:

    def __init__(self):
        self.__cached_dirs = {}

    def add_dir(self, cache_dir):
        self.__cached_dirs[cache_dir] = {}

    def force_delete(self, cache_dir):
        import shutil

        LOG.info('Attempting to delete {}'.format(cache_dir))

        if cache_dir not in self.__cached_dirs:
            pass

        shutil.rmtree(cache_dir, ignore_errors=True)

        LOG.info('<!> {} deleted'.format(cache_dir))

    def strategy(self):
        """
            Removes cached files which haven't being accessed for 1 year or more
        """

        one_year_ago_timestamp = datetime.datetime.timestamp(self.year_ago(1))
        for d in self.__cached_dirs.keys():
            for dir_path in glob('{}/*'.format(d)):
                self.__cached_dirs[d] = {}
                self.__cached_dirs[d][DIR_PATH] = dir_path
                self.__cached_dirs[d][ACCESS] = self.__last_access(dir_path)
                if self.__cached_dirs[d][ACCESS] <= one_year_ago_timestamp:
                    self.force_delete(self.__cached_dirs[d][DIR_PATH])

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
        return datetime.datetime.now() + datetime.timedelta(days=years*365)

    def year_ago(self, years: int = 1):
        return datetime.datetime.now() - datetime.timedelta(days=years*365)
