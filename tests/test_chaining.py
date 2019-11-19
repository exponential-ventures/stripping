import uuid
from unittest import TestCase

from stripping import setup_stripping


class ChainingTestCase(TestCase):

    def test_chain(self):
        tmp_dir = f"/tmp/{str(uuid.uuid4())}/cache/"

        st, context = setup_stripping(tmp_dir)

        @st.chain
        def test_chain_step_1():
            return "Hello"

        @st.chain
        def test_chain_step_2(prefix: str):
            return prefix + " World!"

        r = st.execute()
        self.assertEqual('Hello World!', r)

    def test_mixed_chain(self):
        tmp_dir = f"/tmp/{str(uuid.uuid4())}/cache/"

        st, context = setup_stripping(tmp_dir)
        st.steps = list()
        st.chain_steps = list()

        @st.step
        def test_step_1():
            print("Running regular step #1.")

        @st.chain
        def test_chain_step_1():
            return "Hello"

        @st.chain
        def test_chain_step_2(prefix: str):
            message = prefix + " World!"
            print(message)
            return message

        @st.step
        def test_step_2():
            print("Running regular step #2.")

        r = st.execute()

        # Since the last step is not a chain and it doesn't return anything, the execute result is empty.
        self.assertEqual(None, r)
