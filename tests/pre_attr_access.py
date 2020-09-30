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


# @st.step()
# def save_new_version_9d122046_e311_4125_baa7_128eb59d048d():
#     new_name = f"iris_0_1_0.csv"
#     ctx.ds.to_csv(new_name, mode="w+", encoding='utf-8', index=False)

st.execute()
