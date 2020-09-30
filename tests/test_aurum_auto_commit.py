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
import shutil
import subprocess
from os.path import split, join

import asynctest
from aurum import git

from stripping import setup_stripping
from stripping.executor import Stripping

tmp_dir = join(split(__file__)[0], '.test_cache')


def set_git_for_test():
    proc = git.run_git('config', '--global', 'user.email', '"test@example.com"', )
    _, err = proc.communicate()

    if proc.returncode != 0:
        raise Exception(err)

    proc = git.run_git('config', '--global', 'user.name', '"test"', )
    _, err = proc.communicate()

    if proc.returncode != 0:
        raise Exception(err)

    logging.debug("Git config successful")


class TestExecutor(asynctest.TestCase):
    def setUp(self):
        self.st, self.ctx = setup_stripping('.stripping')
        self.st.steps = []  # To guarantee no
        # cache from another tests

    def tearDown(self):
        shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_step_decorator_with_commits(self):
        set_git_for_test()
        comp_proc = subprocess.run(
            ["au --verbose init"],
            shell=True,
            capture_output=True,
            encoding="utf-8",
        )

        self.assertEqual(comp_proc.returncode, 0, msg=comp_proc.stderr)

        comp_proc = subprocess.run(
            ["git rev-list --all --count"],
            shell=True,
            capture_output=True,
            encoding="utf-8",
        )

        self.assertEqual(comp_proc.returncode, 0, msg=comp_proc.stderr)
        self.assertEqual(comp_proc.stdout, "2\n")

        @self.st.step(skip_cache=False)
        def test_cache():
            print("aaaa")

        self.assertEqual(1, len(self.st.steps))
        self.assertEqual('test_cache', self.st.steps[0].name)
        self.assertIn('print("aaaa")\n', self.st.steps[0].code)

        self.st.execute()

        comp_proc = subprocess.run(
            ["git rev-list --all --count"],
            shell=True,
            capture_output=True,
            encoding="utf-8",
        )

        self.assertEqual(comp_proc.returncode, 0, msg=comp_proc.stderr)
        self.assertEqual(comp_proc.stdout, "2\n")
