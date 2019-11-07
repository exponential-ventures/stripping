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
import logging
import os
import pickle
import sys
from pathlib import Path
from typing import Iterable

from catalysis.storage import StorageClient

from .exceptions import StepNotCached

LOG = logging.getLogger('stripping')


class CacheStorage:
    return_file_name = "step_return"
    context_file_name = "context"

    def __init__(self, cache_dir: str, catalysis_credential_name: str = '') -> None:
        self.cache_dir = cache_dir

        if catalysis_credential_name != '':
            self.catalysis_client = StorageClient(catalysis_credential_name)
        else:
            self.catalysis_client = None

        # Only create cache_dir if we don't have a catalysis client, otherwise the driver already takes
        # care of creating our directories whenever we write to a file with non-existent path.
        if self.catalysis_client is None and not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        self.exec_name = os.path.split(sys.argv[0])[1]
        self.hashed_name = hashlib.sha1(self.exec_name.encode()).hexdigest()
        self.exec_args = sorted(sys.argv[1:])
        self.hashed_args = hashlib.sha1(",".join(self.exec_args).encode()).hexdigest()

    def step_location(self, step_code: str, *args, **kwargs) -> Iterable[Path]:
        input_args = list(args) + [i for pair in sorted(kwargs.items(), key=lambda x: x[0]) for i in pair]
        input_args = ",".join([str(i) for i in input_args]).encode()
        loc = Path(os.path.join(self.cache_dir,
                                self.hashed_name,
                                self.hashed_args,
                                hashlib.sha1(step_code.encode()).hexdigest(),
                                hashlib.sha1(input_args).hexdigest()))
        return loc, loc / 'return', loc / 'context'

    def get_step(self, step_name: str, step_code: str, context, *args, **kwargs):
        location, return_location, context_location = self.step_location(step_code, *args, **kwargs)
        return_file_name = return_location / '0'

        if location.exists():
            if context_location.exists():
                context.register_context_location(context_location)

            if return_file_name.exists():
                with open(return_file_name, 'rb') as return_file:
                    try:
                        return pickle.load(return_file)
                    except EOFError:
                        # Step returned None, which can't be properly pickled.
                        return None

            return None

        raise StepNotCached(f"The step '{step_name}' is not yet cached.")

    def save_step(self, step_code: str, step_return, context, *args, **kwargs) -> None:
        location, return_location, context_location = self.step_location(step_code, *args, **kwargs)

        if not location.exists():
            os.makedirs(location)
        if not return_location.exists():
            os.makedirs(return_location)
        if not context_location.exists():
            os.makedirs(context_location)

        if step_return is not None:
            with open(return_location / '0', 'wb') as return_file:
                pickle.dump(step_return, return_file)

        context.register_context_location(context_location)
        context.serialize()
