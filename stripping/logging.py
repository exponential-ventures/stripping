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
