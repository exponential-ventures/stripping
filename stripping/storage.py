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


import asyncio
import hashlib
import logging
import os
import pickle
import sys
from pathlib import Path
from tempfile import TemporaryFile
from typing import Iterable

try:
    from catalysis.storage import StorageClient

    has_catalysis = True
except ImportError:
    has_catalysis = False

from .exceptions import StepNotCached

LOG = logging.getLogger('stripping')


class CacheStorage:
    return_file_name = "step_return"
    context_file_name = "context"

    def __init__(self, cache_dir: str, catalysis_credential_name: str = '') -> None:
        self.cache_dir = cache_dir

        if has_catalysis and catalysis_credential_name != '':
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

        if self.catalysis_client is not None:
            with self.catalysis_client.open(location) as c_local:
                if c_local.exists():

                    with self.catalysis_client.open(context_location) as c_context:
                        if c_context.exists():
                            context.register_context_location(context_location)

                    with self.catalysis_client.open(return_file_name, 'rb') as c_return:
                        if c_return.exists():
                            try:
                                outfile = TemporaryFile()
                                outfile.write(c_return.read())

                                return pickle.load(outfile)
                            except EOFError:
                                # Step returned None, which can't be properly pickled.
                                return None

                    return None
        else:
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

        # Only create dirs if we don't have a catalysis client, otherwise the driver already takes
        # care of creating our directories whenever we write to a file with non-existent path.
        if self.catalysis_client is None:
            if not location.exists():
                os.makedirs(location)
            if not return_location.exists():
                os.makedirs(return_location)
            if not context_location.exists():
                os.makedirs(context_location)

        if step_return is not None:

            if self.catalysis_client is not None:
                with self.catalysis_client.open(return_location / '0', mode='wb+') as f:
                    asyncio.create_task(f.write(pickle.dumps(step_return)))
            else:
                with open(return_location / '0', 'wb') as return_file:
                    pickle.dump(step_return, return_file)

        context.register_context_location(context_location)
        context.register_catalysis_client(self.catalysis_client)
        context.serialize()
