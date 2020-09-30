#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
# ----------------
# |              |
# | CONFIDENTIAL |
# |              |
# ----------------
##
# Copyright Exponential Ventures LLC (C), 2019 All Rights Reserved
##
# Author: Thales Ribeiro <thales@xnv.io>
##
# If you do not have a written authorization to read this code
# PERMANENTLY REMOVE IT FROM YOUR SYSTEM IMMEDIATELY.
##

import logging
import os
from logging.config import fileConfig
from pathlib import Path
import sys
from stripping.singleton import SingletonDecorator


@SingletonDecorator
class Logging:
    def __init__(self):
        self.file_name = 'logging.ini'
        try:
            fileConfig(self.__find_config_file())
        except FileNotFoundError:
            logging.info("Logging file not found. Logging to stdout.")
            logging.StreamHandler(sys.stdout)

    def get_logger(self):
        return logging.getLogger('stripping')

    def __find_config_file(self) -> str:
        cwd = Path(os.getcwd())
        checked_paths = []
        for parent in [cwd] + list(cwd.parents):
            tentative_config_location = (parent / self.file_name)
            tentative_config_location2 = (parent / "conf" / self.file_name)
            if tentative_config_location.exists():
                return tentative_config_location
            elif tentative_config_location2.exists():
                return tentative_config_location2
            checked_paths.append(str(tentative_config_location))
            checked_paths.append(str(tentative_config_location2))
        raise FileNotFoundError("Logging config file could not be found. "
                                "Checked locations: {}".format(", ".join(checked_paths)))
