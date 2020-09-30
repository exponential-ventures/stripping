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


import numpy as np
import pandas as pd
from math import e
import logging

logging = logging.getLogger('stripping')


def avg(df: pd.DataFrame):
    return df.mean()


def std(df: pd.DataFrame):
    return df.std()


def max(df: pd.DataFrame):
    return df.max()


def min(df: pd.DataFrame):
    return df.min()


def count(df: pd.DataFrame):
    return df.count()


def count_null(df: pd.DataFrame):
    return df.isnull().sum()


def count_notnull(df: pd.DataFrame):
    return df.notnull().sum()


def max_length(df: pd.DataFrame):
    measurer = np.vectorize(len)
    columns_max_length = {}
    aux = df.select_dtypes(exclude=['int', 'bool', 'float64', 'int64'])
    for k in aux.keys():
        try:
            columns_max_length[k] = measurer(aux[k]).max()
        except Exception as err:
            logging.error(f"Elemental filter max_length, columns {k}, {str(err)}")

    return columns_max_length


def min_length(df: pd.DataFrame):
    measurer = np.vectorize(len)
    columns_min_length = {}
    aux = df.select_dtypes(exclude=['int', 'bool', 'float64', 'int64'])
    for k in aux.keys():
        try:
            columns_min_length[k] = measurer(aux[k]).min()
        except Exception as err:
            logging.error(f"Elemental filter min_length, columns {k}, {str(err)}")

    return columns_min_length


def avg_length(df: pd.DataFrame):
    measurer = np.vectorize(len)
    columns_avg_length = {}
    aux = df.select_dtypes(exclude=['int', 'bool', 'float64', 'int64'])
    for k in aux.keys():
        try:
            columns_avg_length[k] = measurer(aux[k]).mean()
        except Exception as err:
            logging.error(f"Elemental filter min_length, columns {k}, {str(err)}")

    return columns_avg_length


def number_uniques(df: pd.DataFrame):
    return df.nunique()


def memory_size(df: pd.DataFrame):
    return df.memory_usage(deep=True, index=False)


def memory_avg(df: pd.DataFrame):
    number_of_rows = df.shape[0]
    avg_types = {}
    types = ['int', 'int64', 'bool', 'float64', 'float32']
    for k in df.keys():
        field = df[k]
        if field.dtype not in types:
            avg_types[k] = field.memory_usage(deep=True) / number_of_rows
        else:
            avg_types[k] = field.dtype.itemsize

    return avg_types


def describe(df: pd.DataFrame):
    return df.describe()


def sample(df: pd.DataFrame):
    return df.sample(n=20)


def median(df: pd.DataFrame):
    return df.median()


def gini_index(df: pd.DataFrame):
    gini_index = {}
    for k in df.keys():
        probalities = df[k].value_counts(normalize=True)
        gini_index[k] = 1 - np.sum(np.square(probalities))

    return gini_index


def entrophy_gain(df: pd.DataFrame):
    gain = {}
    for k in df.keys():
        base = None
        value_counts = df[k].value_counts(normalize=True, sort=False)
        base = e if base is None else base
        gain[k] = -(value_counts * np.log(value_counts) / np.log(base)).sum()
    return gain


def entrophy_index(df: pd.DataFrame):
    index = {}
    for k in df.keys():
        probabilities = df[k].value_counts(normalize=True)
        index[k] = -1 * np.sum(np.log2(probabilities) * probabilities)
    return index


def frequency(df: pd.DataFrame):
    frequencies = {}
    for k in df.keys():
        frequencies[k] = df[k].value_counts().to_dict()

    return frequencies


def field_types(df: pd.DataFrame):
    return df.dtypes


filters = [avg, std, max, min, count, count_null, count_notnull, median, entrophy_index, entrophy_gain, gini_index,
           frequency, field_types, max_length, min_length, avg_length, number_uniques, memory_size, memory_avg, sample]
