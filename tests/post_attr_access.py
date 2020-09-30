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


from pathlib import Path

import pandas as pd

from stripping import setup_stripping

file_path = "iris.csv"
current_dir = Path(__file__).parent.absolute()
st, ctx = setup_stripping('.stripping')


@st.step()
def load_dataset():
    ctx.ds = pd.read_csv(file_path)
    # ctx.ds = pd.DataFrame([1, 2, 3, 4])
    # ctx.ds = pd.DataFrame({'name': ["a", "b", "c", "d", "e", "f", "g"],
    #                        'age': [20, 27, 35, 55, 18, 21, 35],
    #                        'designation': ["VP", "CEO", "CFO", "VP", "VP", "CEO", "MD"]})
    # with open(file_path, "r") as f:
    #     ctx.ds = pd.read_csv(f.read())



@st.step()
def access_ctx_ds():
    print(ctx.ds)


st.execute()
