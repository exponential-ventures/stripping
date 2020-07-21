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
import shutil
import subprocess
from pathlib import Path
from shutil import copyfile

import asynctest

current_dir = Path(__file__).parent.absolute()


class TestAttrFileDeserializing(asynctest.TestCase):

    def tearDown(self):
        shutil.rmtree(os.path.join(current_dir, "log"), ignore_errors=True)
        os.remove(os.path.join(current_dir, "attr_access.py"))

    def setUp(self) -> None:
        os.mkdir(os.path.join(current_dir, "log"))

    def test_accessing_serialized_attrs(self):
        copyfile(os.path.join(current_dir, "pre_attr_access.py"), os.path.join(current_dir, "attr_access.py"))

        proc = subprocess.Popen(
            ["python", "attr_access.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            cwd=current_dir,
        )
        _, error = proc.communicate()
        self.assertEqual(error, b'')

        copyfile(os.path.join(current_dir, "post_attr_access.py"), os.path.join(current_dir, "attr_access.py"))

        proc = subprocess.Popen(
            ["python", "attr_access.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            cwd=current_dir,
        )

        out, error = proc.communicate()

        if error != b'':
            print(error.decode())
        else:
            print(out.decode())

        self.assertEqual(error, b'')
