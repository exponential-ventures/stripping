import os
import shutil
import subprocess
from pathlib import Path
from shutil import copyfile

import asynctest

current_dir = Path(__file__).parent.absolute()


class TestWeirdBug(asynctest.TestCase):

    def tearDown(self):
        shutil.rmtree(os.path.join(current_dir, "log"), ignore_errors=True)
        os.remove(os.path.join(current_dir, "bug.py"))

    def setUp(self) -> None:
        os.mkdir(os.path.join(current_dir, "log"))

    def test_bug(self):
        copyfile(os.path.join(current_dir, "non_buggy_script.py"), os.path.join(current_dir, "bug.py"))

        proc = subprocess.Popen(
            ["python", "bug.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            cwd=current_dir,
        )
        _, error = proc.communicate()
        self.assertEqual(error, b'')

        copyfile(os.path.join(current_dir, "buggy_script.py"), os.path.join(current_dir, "bug.py"))

        proc = subprocess.Popen(
            ["python", "bug.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            cwd=current_dir,
        )

        _, error = proc.communicate()
        print(error)
        # self.assertEqual(error, b'')
