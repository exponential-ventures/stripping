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
import os

from catalysis.common.configuration import ClientConfiguration

from .cache import StepCache
from .executor import Stripping, Context
from .logging import Logging

logging = Logging().get_logger()


def setup_stripping(cache_dir: str = None):
    if cache_dir is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        cache_dir = os.path.join(current_dir, 'stripping_cache')
        logging.info(f"No cache_dir was specified, using default location: {cache_dir}")

    st, c = Stripping(cache_dir), Context()
    st.cache.register_context(c)
    return st, c


def setup_stripping_with_catalysis(catalysis_credential_name: str, cache_dir: str = None):
    if cache_dir is None:
        cache_dir = fetch_catalysis_default_location(catalysis_credential_name)

    st, c = Stripping(cache_dir, catalysis_credential_name), Context()
    st.cache.register_context(c)
    return st, c


def fetch_catalysis_default_location(catalysis_credential_name: str):
    credential = ClientConfiguration().get_credential(catalysis_credential_name)
    if 'path' not in credential.keys():
        raise RuntimeError(
            "No cache_dir was supplied to catalysis and we were not able to find the default path in your config"
        )

    return credential['path']
