import uuid
from unittest import TestCase

from stripping import setup_stripping

tmp_dir = f"/tmp/{str(uuid.uuid4())}/cache/"

st, context = setup_stripping(tmp_dir)


@st.step(chain=True)
def test_chain_step_1():
    return "Hello"


class ChainingTestCase(TestCase):

    def test_chain(self):
        r = st.execute()
        self.assertEqual('Hello', r)
