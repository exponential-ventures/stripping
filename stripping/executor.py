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


import asyncio
import inspect
import pickle
import numpy as np

from io import StringIO

from .cache import StepCache
from .singleton import SingletonDecorator


@SingletonDecorator
class Context:
    pass


@SingletonDecorator
class Stripping:
    steps = []
    cache = None

    def __init__(self, cache_dir):
        self.cache = StepCache(cache_dir)

    def step(self, step_fn):
        async def wrapper(*args, **kwargs):
            result = step_fn(*args, **kwargs)

            return result

        wrapper.code = inspect.getsource(step_fn)

        self.steps.append(wrapper)
        return wrapper

    def execute(self):
        asyncio.get_event_loop().run_until_complete(self._execute())

    async def _execute(self):
        for i in range(len(self.steps)):
            results = await self.cache.execute_or_retrieve(self.steps[i])
