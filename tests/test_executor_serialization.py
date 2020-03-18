import shutil
from os.path import split, join

import asynctest
import pandas as pd

from stripping import setup_stripping

tmp_dir = join(split(__file__)[0], '.test_cache')


class TestExecutorSerialization(asynctest.TestCase):

    def tearDown(self):
        shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_step_decorator(self):
        st, ctx = setup_stripping(tmp_dir)
        st.steps = []  # To guarantee no cache from another tests

        @st.step()
        def test_cache():
            ctx.df = pd.DataFrame()

        st.execute()

        st.steps = []

        @st.step()
        def test_cache2():
            print(ctx.df)

        st.execute()
        ctx.deserialize()
