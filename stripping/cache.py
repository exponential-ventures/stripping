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
##
## If you do not have a written authorization to read this code
## PERMANENTLY REMOVE IT FROM YOUR SYSTEM IMMEDIATELY.
##


import inspect
import logging

from .exceptions import StepNotCached
from .singleton import SingletonDecorator
from .storage import CacheStorage

LOG = logging.getLogger('stripping')


@SingletonDecorator
class StepCache:
    context = None

    def __init__(self, cache_dir):
        self.cache_dir = cache_dir
        self.storage = CacheStorage(self.cache_dir)

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

            self.storage.save_step(step_fn.code, step_return, self.context, *args, **kwargs)

            return step_return
