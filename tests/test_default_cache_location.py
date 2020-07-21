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


from unittest import TestCase

from stripping import setup_stripping, setup_stripping_with_catalysis


class DefaultCacheLocationTestCase(TestCase):

    def test_default_location_wo_catalysis(self):
        st, _ = setup_stripping()
        self.assertEqual(
            "/usr/src/app/stripping/stripping_cache",
            st.cache.cache_dir,
        )

    def test_default_location_with_catalysis(self):
        st, _ = setup_stripping_with_catalysis(catalysis_credential_name="local")
        self.assertEqual(
            "/tmp/list/",
            st.cache.cache_dir,
        )
