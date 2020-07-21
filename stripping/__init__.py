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
