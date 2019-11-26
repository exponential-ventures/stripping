import numpy as np
from pandas.core.frame import DataFrame


def avg(df: DataFrame):
    return df.mean()


def std(df: DataFrame):
    return df.std()


def max(df: DataFrame):
    return df.max()


def min(df: DataFrame):
    return df.min()


def count(df: DataFrame):
    return df.count()


def count_null(df: DataFrame):
    return df.isnull().sum()


def count_notnull(df: DataFrame):
    return df.notnull().sum()


def max_length(df: DataFrame):
    measurer = np.vectorize(len)
    columns_max_length = {}
    aux = df.select_dtypes(exclude=['int', 'bool', 'float64'])
    for k in aux.keys():
        columns_max_length[k] = measurer(aux[k]).max()

    return columns_max_length


def min_length(df: DataFrame):
    measurer = np.vectorize(len)
    columns_min_length = {}
    aux = df.select_dtypes(exclude=['int', 'bool', 'float64'])
    for k in aux.keys():
        columns_min_length[k] = measurer(aux[k]).min()

    return columns_min_length


def avg_length(df: DataFrame):
    measurer = np.vectorize(len)
    columns_avg_length = {}
    aux = df.select_dtypes(exclude=['int', 'bool', 'float64'])
    for k in aux.keys():
        columns_avg_length[k] = measurer(aux[k]).mean()

    return columns_avg_length


def number_uniques(df: DataFrame):
    return df.nunique()


def memory_size(df: DataFrame):
    return df.memory_usage(deep=True, index=False)


def memory_avg(df: DataFrame):
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
