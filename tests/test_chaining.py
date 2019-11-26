from unittest import TestCase

from tests.utils import set_up_stripping_for_tests


class ChainingTestCase(TestCase):

    def test_chain_only(self):
        st, context = set_up_stripping_for_tests()

        @st.chain
        def test_chain_step_1():
            return "Hello"

        @st.chain
        def test_chain_step_2(prefix: str):
            return prefix + " World!"

        r = st.execute()
        self.assertEqual('Hello World!', r)

    def test_mixed_chain(self):
        st, context = set_up_stripping_for_tests()

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

    def test_regular_steps_only(self):
        st, context = set_up_stripping_for_tests()

        @st.step
        def test_step_1():
            print("Running regular step #1.")

        @st.step
        def test_step_2():
            print("Running regular step #2.")

        @st.step
        def test_step_3():
            print("Running regular step #3.")

        r = st.execute()
        self.assertEqual(None, r)
