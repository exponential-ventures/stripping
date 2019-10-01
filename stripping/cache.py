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

from .exceptions import StepNotCached
from .singleton import SingletonDecorator
from .storage import CacheStorage


@SingletonDecorator
class StepCache:
    context = None

    def __init__(self, cache_dir):
        self.cache_dir = cache_dir
        self.storage = CacheStorage(self.cache_dir)

    def register_context(self, context):
        self.context = context

    async def execute_or_retrieve(self, step_fn, *args, **kwargs):
        step_code = inspect.getsource(step_fn)

        try:
            return self.storage.get_step(step_code, *args, **kwargs)
        except StepNotCached():
            step_return = None

            if inspect.iscoroutinefunction(step_fn):
                step_return = await step_fn(*args, **kwargs)
            else:
                step_return = step_fn(*args, **kwargs)

            self.storage.save_step(step_code, step_return, self.context, *args, **kwargs)

            return step_return
