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


import hashlib
import inspect
import os
import sys

from .singleton import SingletonDecorator


@SingletonDecorator
class StepCache:
    context = None

    def __init__(self, cache_dir):
        self.cache_dir = cache_dir


    def register_context(self, context):
        self.context = context

    async def execute_or_retrieve(self, step_fn, *args, **kwargs):
        print(step_fn.code)
        print(hashlib.sha1(step_fn.code.encode()).hexdigest())

        if inspect.iscoroutinefunction(step_fn):
            return await step_fn(*args, **kwargs)

        return step_fn(*args, **kwargs)
