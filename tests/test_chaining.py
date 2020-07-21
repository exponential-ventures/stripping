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


import uuid
from unittest import TestCase

from stripping import setup_stripping


class ChainingTestCase(TestCase):

    def test_chain_only(self):
        st, context = self._setUpStripping()

        @st.chain
        def test_chain_step_1():
            return "Hello"

        @st.chain
        def test_chain_step_2(prefix: str):
            return prefix + " World!"

        r = st.execute()
        self.assertEqual('Hello World!', r)

    def test_mixed_chain(self):
        st, context = self._setUpStripping()

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
        st, context = self._setUpStripping()

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

    @staticmethod
    def _setUpStripping():
        tmp_dir = f"/tmp/{str(uuid.uuid4())}/cache/"

        st, context = setup_stripping(tmp_dir)

        # Resetting lists to prevent cross-test contamination
        st.steps = list()
        st.chain_steps = list()

        return st, context
