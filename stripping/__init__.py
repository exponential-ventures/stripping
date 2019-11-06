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


from .cache import StepCache
from .executor import Stripping, Context
from .logging import Logging

Logging().get_logger()


def setup_stripping(cache_dir):
    st, c = Stripping(cache_dir), Context()
    st.cache.register_context(c)
    return st, c
