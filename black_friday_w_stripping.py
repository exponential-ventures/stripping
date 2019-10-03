#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
## ----------------
## |              |
## | CONFIDENTIAL |
## |              |
## ----------------
##
## Copyright Exponential Ventures LLC (C), 2019 All Rights Reserved
##
## Author: Adriano Marques <adriano@xnv.io>
##
## If you do not have a written authorization to read this code
## PERMANENTLY REMOVE IT FROM YOUR SYSTEM IMMEDIATELY.
##


from os.path import split, join

from stripping import setup_stripping

st, c = setup_stripping(join(split(__file__)[0], '.stripping'))


@st.step
def load_dataset():
    print("Load Dataset")
    c.ds = [1, 2, 3, 4, 5]
    print(c.ds)


@st.step
def split_dataset():
    print("Split Dataset")
    print(c.ds)
    c.ds += [6, 7, 8, 9, 10]


@st.step
def encode_labels():
    print("Encode Labels...")
    c.ds += [11, 12, 13, 14, 15]
    print(c.ds)


@st.step
def scale_values():
    print("Scale Values")
    c.ds += [16, 17, 18, 19, 20]
    print(c.ds)


@st.step
def train_model():
    print("Training model")
    print(c.ds)
    c.error = 0.1


@st.step
def measure_error():
    print("Measuring error")
    print(c.error)


@st.step
def final_report():
    print("Final report:")
    print("Howdy ho!")

st.execute()