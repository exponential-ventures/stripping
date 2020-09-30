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


from stripping.benchmark import Benchmark
benchmark = Benchmark('Black Friday with stripping')
benchmark.start()

import logging
from os.path import split, join

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

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
    c.X_train, c.X_test, c.y_train, c.y_test = train_test_split(
        c.X, c.y, test_size=0.15, random_state=0)


@st.step()
def encode_labels():
    #################################
    # Encoding non-numerical columns
    c.x_train_encoder = LabelEncoder()
    c.X_train[:, 0] = c.x_train_encoder.fit_transform(c.X_train[:, 0])
    c.X_train[:, 1] = c.x_train_encoder.fit_transform(c.X_train[:, 1])
    c.X_train[:, 3] = c.x_train_encoder.fit_transform(c.X_train[:, 3])
    c.X_train[:, 4] = c.x_train_encoder.fit_transform(c.X_train[:, 4])

    c.x_test_encoder = LabelEncoder()
    c.X_test[:, 0] = c.x_test_encoder.fit_transform(c.X_test[:, 0])
    c.X_test[:, 1] = c.x_test_encoder.fit_transform(c.X_test[:, 1])
    c.X_test[:, 3] = c.x_test_encoder.fit_transform(c.X_test[:, 3])
    c.X_test[:, 4] = c.x_test_encoder.fit_transform(c.X_test[:, 4])


@st.step()
def scale_values():
    ######################
    # Scaling all columns
    c.X_train_scaler = StandardScaler()
    c.X_test_scaler = StandardScaler()

    c.X_train = c.X_train_scaler.fit_transform(c.X_train)
    c.X_test = c.X_test_scaler.fit_transform(c.X_test)


@st.step()
def train_model():
    #################################
    # Training and error measurement
    c.regressor = RandomForestRegressor(n_estimators=1000, random_state=0)
    c.regressor.fit(c.X_train, c.y_train)


@st.step()
def measure_error():
    c.y_pred = c.regressor.predict(c.X_test)
    c.error = mean_absolute_error(c.y_test, c.y_pred)


st.execute()
