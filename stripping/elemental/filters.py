import numpy as np
import pandas as pd
from math import e


def avg(dataframe):
    return dataframe.mean()


def std(dataframe):
    return dataframe.std()


def max(dataframe):
    return dataframe.max()


def min(dataframe):
    return dataframe.min()


def count(dataframe):
    return dataframe.count()


def count_null(dataframe):
    return dataframe.isnull().sum()


def count_notnull(dataframe):
    return dataframe.notnull().sum()


def max_length(dataframe):
    measurer = np.vectorize(len)
    columns_max_length = {}
    aux = dataframe.select_dtypes(exclude=['int', 'bool', 'float64'])
    for k in aux.keys():
        columns_max_length[k] = measurer(aux[k]).max()

    return columns_max_length


def min_length(dataframe):
    measurer = np.vectorize(len)
    columns_min_length = {}
    aux = dataframe.select_dtypes(exclude=['int', 'bool', 'float64'])
    for k in aux.keys():
        columns_min_length[k] = measurer(aux[k]).min()

    return columns_min_length


def avg_length(dataframe):
    measurer = np.vectorize(len)
    columns_avg_length = {}
    aux = dataframe.select_dtypes(exclude=['int', 'bool', 'float64'])
    for k in aux.keys():
        columns_avg_length[k] = measurer(aux[k]).mean()

    return columns_avg_length


def number_uniques(dataframe):
    return dataframe.nunique()


def memory_size(dataframe):
    return dataframe.memory_usage(deep=True, index=False)


def memory_avg(dataframe):
    number_of_rows = dataframe.shape[0]
    avg_types = {}
    types = ['int', 'int64', 'bool', 'float64', 'float32']
    for k in dataframe.keys():
        field = dataframe[k]
        if field.dtype not in types:
            avg_types[k] = field.memory_usage(deep=True) / number_of_rows
        else:
            avg_types[k] = field.dtype.itemsize

    return avg_types


def describe(dataframe):
    return dataframe.describe()


def sample(dataframe):
    return dataframe.sample(n=20)


def median(dataframe):
    return dataframe.median()


def gini_index(dataframe):
    gini_index = {}
    for k in dataframe.keys():
        probalities = dataframe[k].value_counts(normalize=True)
        gini_index[k] = 1 - np.sum(np.square(probalities))

    return gini_index


def entrophy_gain(dataframe):
    gain = {}
    for k in dataframe.keys():
        base = None
        value_counts = dataframe[k].value_counts(normalize=True, sort=False)
        base = e if base is None else base
        gain[k] = -(value_counts * np.log(value_counts) / np.log(base)).sum()
    return gain


def entrophy_index(dataframe):
    index = {}
    for k in dataframe.keys():
        probalities = dataframe[k].value_counts(normalize=True)
        index[k] = -1 * np.sum(np.log2(probalities) * probalities)
    return index


def frequency(dataframe):
    frequencies = {}
    for k in dataframe.keys():
        frequencies[k] = dataframe[k].value_counts().to_dict()

    return frequencies


filters = [avg, std, max, min, count, count_null, count_notnull, median, entrophy_index, entrophy_gain, gini_index,
           frequency, max_length, min_length, avg_length, number_uniques, memory_size, memory_avg, sample]
