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
import pickle
from os import makedirs
from os.path import join
from pathlib import Path

import numpy as np

from .exceptions import StepNotCached


class CacheStorage:
    return_file_name = "step_return"
    context_file_name = "context"

    def __init__(self, cache_dir:str) -> None:
        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        self.exec_name = os.path.split(sys.argv[0])[1]
        self.hashed_name = hashlib.sha1(self.exec_name).hexdigest()
        self.exec_args = sorted(sys.argv[1:])
        self.hashed_args = hashlib.sha1(",".join(self.exec_args)).hexdigest()

    def step_location(self, step_code:str, *args, **kwargs) -> Path:
        input_args = args + [i for pair in sorted(kwargs.items(), key=lambda x: x[0]) for i in pair]
        input_args = ",".join([str(i) for i in input_args])
        return Path(join(self.cache_dir,
                         self.hashed_name,
                         self.hashed_args,
                         hashlib.sha1(step_code).hexdigest(),
                         hashlib.sha1(input_args).hexdigest()))

    def get_step(self, step_code:str, *args, **kwargs):
        step_name = step_code  # TODO extract step name
        location = self.step_location(step_code, *args, **kwargs)
        if location.exists():
            return  # TODO: open the pickles for context and return value of the step

        raise StepNotCached("The step {} is not yet cached.".format(step_name))

    def save_step(self, step_code:str, step_return, context, *args, **kwargs) -> None:
        location = self.step_location(step_code, *args, **kwargs)
        if not location.exists():
            makedirs(location)

    def __serialize(self) -> dict:
        serialized = {}
        for attr in dir(self):
            if attr.startswith("__"):
                continue

            attribute = getattr(self, attr)
            if inspect.isfunction(attribute):
                continue

            serialized[attr] = StringIO()
            if isinstance(attribute, np.ndarray):
                np.save(serialized[attr], attribute)  # TODO: Serialize straight to local cache to save mem
            else:
                pickle.dump(attr, serialized[attr])  # TODO: Serialize straight to local cache to save mem

        return serialized

    def __deserialize(self, serialized: dict) -> None:
        for name, attr in serialized.items():
            try:
                setattr(self, name, pickle.load(attr))  # TODO: read straight from local file cached to save mem
            except:
                setattr(self, name, np.load(attr))  # TODO: read straight from local file cached to save mem

