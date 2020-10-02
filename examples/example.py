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
from os.path import split, join

import pandas as pd

from stripping import setup_stripping

st, c = setup_stripping(join(split(__file__)[0], '.stripping'))
logging.basicConfig(level=logging.DEBUG)


@st.step()
def load_dataset():
    c.bf_file = join(split(__file__)[0], "datasets", "black_friday.csv")
    logging.info(f"Processing file '{c.bf_file}' without using the Catalysis acceleration framework.")
    c.bf = pd.read_csv(c.bf_file)


@st.step()
def split_dataset():
    c.X = c.bf.iloc[:, 0:6].values
    c.y = c.bf.iloc[:, 9].values

@st.step()
def hello_stripping():
    print('Hellow')

st.execute()
