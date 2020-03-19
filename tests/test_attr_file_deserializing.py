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
