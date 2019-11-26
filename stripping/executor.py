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
import logging
import os
import pickle
from tempfile import TemporaryFile

import numpy as np
from catalysis.storage import StorageClient
from pandas import DataFrame

from stripping.elemental import Elemental
from .cache import StepCache
from .singleton import SingletonDecorator

logging = logging.getLogger('stripping')


@SingletonDecorator
class Context:
    __context_location = None
    catalysis_client = None

    def register_context_location(self, context_location):
        self.__context_location = context_location

    def register_catalysis_client(self, client):
        self.catalysis_client = client

    def __getattr__(self, attr_name):
        attr_file_name = os.path.join(self.__context_location, attr_name)

        if self.catalysis_client is not None:

            with self.catalysis_client.open(attr_file_name) as f:
                if f.exists():
                    self._deserialize(attr_file_name)
                    return getattr(self, attr_name)
        else:

            if os.path.exists(attr_file_name):
                self._deserialize(attr_file_name)
                return getattr(self, attr_name)

        logging.warning(f"Attribute '{attr_name}' was not found.")
        raise AttributeError(f"Attribute '{attr_name}' was not found.")

    def serialize(self) -> None:
        for attr in dir(self):
            if attr.startswith("_") or attr == 'self':
                continue

            attribute = getattr(self, attr)
            if inspect.ismethod(attribute):
                continue

            if isinstance(attribute, StorageClient):
                continue

            context_file_name = os.path.join(self.__context_location, attr)
            logging.info(f"Serializing context attribute '{attr}' to '{context_file_name}'...")
            if self.catalysis_client is not None:
                with self.catalysis_client.open(context_file_name, 'wb') as attr_file:
                    if isinstance(attribute, np.ndarray):
                        logging.debug(f"Context Attribute '{attr}' is a numpy array.")
                        outfile = TemporaryFile()
                        np.save(outfile, attribute)
                        with open(outfile) as tf:
                            attr_file.write(tf.read())
                    else:
                        logging.debug(f"Context Attribute '{attr}' is a python object of type '{type(attribute)}'.")
                        attr_file.write(pickle.dumps(attribute))
            else:
                with open(context_file_name, 'wb') as attr_file:
                    if isinstance(attribute, np.ndarray):
                        logging.debug(f"Context Attribute '{attr}' is a numpy array.")
                        np.save(attr_file, attribute)
                    else:
                        logging.debug(f"  Context Attribute '{attr}' is a python object of type '{type(attribute)}'.")
                        pickle.dump(attribute, attr_file)

    def deserialize(self) -> None:

        if self.catalysis_client is not None:
            with self.catalysis_client.open(self.__context_location) as cc:
                for attr_file_name in cc.list():
                    self._deserialize(os.path.join(self.__context_location, attr_file_name))
        else:
            for attr_file_name in os.listdir(self.__context_location):
                self._deserialize(os.path.join(self.__context_location, attr_file_name))

    def _deserialize(self, attr_file_name):
        logging.info(f"Deserializing context attribute from '{attr_file_name}'")

        # TODO Refactor this to be more elegant
        if self.catalysis_client is not None:
            with self.catalysis_client.open(attr_file_name, 'rb') as attr_file:
                try:
                    logging.debug(f"Attempting to deserialize '{attr_file_name}' with pickle...")
                    setattr(self, attr_file_name, pickle.load(attr_file))
                    logging.debug(
                        f"Successfully deserialized '{attr_file_name}' as a python object of "
                        f"type '{type(getattr(self, attr_file_name))}'")
                except Exception:
                    logging.debug(f"Attempting to deserialize '{attr_file_name}' with numpy...")
                    setattr(self, attr_file_name, np.load(attr_file))
                    logging.debug(f"Successfully deserialized '{attr_file_name}' as a numpy array.")
        else:
            with open(attr_file_name, 'rb') as attr_file:
                try:
                    logging.debug(f"Attempting to deserialize '{attr_file_name}' with pickle...")
                    setattr(self, attr_file_name, pickle.load(attr_file))
                    logging.debug(
                        f"Successfully deserialized '{attr_file_name}' as a python object of "
                        f"type '{type(getattr(self, attr_file_name))}'")
                except Exception:
                    logging.debug(f"Attempting to deserialize '{attr_file_name}' with numpy...")
                    setattr(self, attr_file_name, np.load(attr_file))
                    logging.debug(f"Successfully deserialized '{attr_file_name}' as a numpy array.")


@SingletonDecorator
class Stripping:
    steps = list()
    chain_steps = list()
    cache = None
    elemental = None

    def __init__(self, cache_dir: str, catalysis_credential_name: str = ''):
        self.cache = StepCache(cache_dir, catalysis_credential_name)

    def step(self, *args, **kwargs):
        step_fn = None

        if len(args) == 1 and callable(args[0]):
            step_fn = args[0]

        skip_cache = kwargs.get('skip_cache', False)
        chain = kwargs.get('chain', False)

        def step_decorator(step_fn):
            async def wrapper(*args, **kwargs):

                previous_result = None

                if self.get_chained_step(step_fn) is not None:

                    last_step = self.get_chained_step(step_fn)

                    if inspect.iscoroutinefunction(last_step):
                        previous_result = await last_step()
                    else:
                        previous_result = last_step()

                if inspect.iscoroutinefunction(step_fn):

                    if chain and previous_result is not None:
                        result = await step_fn(previous_result)
                    else:
                        result = await step_fn(*args, **kwargs)

                else:

                    if chain and previous_result is not None:
                        result = step_fn(previous_result)
                    else:
                        result = step_fn(*args, **kwargs)

                # Explicit type check necessary since object based 'truth' values are unreliable (ie bool(pd.DataFrame))
                if result is not None:
                    return result

                # Explicit type check necessary since object based 'truth' values are unreliable (ie bool(pd.DataFrame))
                if previous_result is not None:
                    return previous_result

            wrapper.code = inspect.getsource(step_fn)
            wrapper.name = step_fn.__name__
            wrapper.skip_cache = skip_cache
            wrapper.chain = chain
            self.steps.append(wrapper)
            if chain:
                self.chain_steps.append(wrapper)

            return wrapper

        return step_decorator(step_fn) if step_fn else step_decorator

    def chain(self, *args, **kwargs):
        kwargs.update({"chain": True})
        return self.step(*args, **kwargs)

    def elemental_step(self, name: str, path=None, report_type=None):
        if len(self.steps) < 1:
            raise RuntimeError("Elemental needs at least one step to provide it's dataset.")

        ds = asyncio.get_event_loop().run_until_complete(self.cache.execute_or_retrieve(self.steps[-1]))
        if not isinstance(ds, DataFrame):
            raise RuntimeError("Last step does not return a valid pandas.DataFrame object to use in Elemental")

        self.elemental = Elemental(ds)
        self.elemental.analyze()
        report_kwargs = {
            'catalysis_client': self.cache.storage.catalysis_client,
            'name': name,
        }

        if path:
            report_kwargs.update({"path": path})

        if report_type:
            report_kwargs.update({"report_type": report_type})

        self.elemental.report(**report_kwargs)

    def execute(self):
        return asyncio.get_event_loop().run_until_complete(self._execute())

    async def _execute(self):

        result = None

        for i in range(len(self.steps)):
            result = await self.cache.execute_or_retrieve(self.steps[i])

        return result

    def get_chained_step(self, current_step):

        for i, step in enumerate(self.chain_steps):
            if step.name == current_step.__name__:

                if i - 1 >= 0:
                    previous_step = self.chain_steps[i - 1]
                    return previous_step

        return None
