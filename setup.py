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
## Author: Thales Ribeiro <thales@xnv.io>
##
## If you do not have a written authorization to read this code
## PERMANENTLY REMOVE IT FROM YOUR SYSTEM IMMEDIATELY.
##

import os
from setuptools import setup, find_packages

setup(
    name='stripping',
    version='0.1.1',
    description='An easy to use pipeline solution for AI/ML experiments',
    author='Adriano Marques, Nathan Martins, Thales Ribeiro',
    author_email='adriano@xnv.io, nathan@xnv.io, thales@xnv.io',
    python_requires='>=3.7.0',
    install_requires=['catalysis-client', 'numpy'],
    include_package_data=True,
    url='https://github.com/exponential-ventures/stripping',
    packages=find_packages(exclude=['*tests*', 'test*']),
    platforms=['any'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],

)
