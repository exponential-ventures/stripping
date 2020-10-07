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


import os
from setuptools import setup, find_packages

setup(
    name='stripping',
    version='0.2.1',
    description='An easy to use pipeline solution for AI/ML experiments',
    author='Adriano Marques, Nathan Martins, Thales Ribeiro',
    author_email='adriano@xnv.io, nathan@xnv.io, thales@xnv.io',
    python_requires='>=3.7.0',
    install_requires=['aurum', 'numpy'],
    include_package_data=True,
    license="GNU LGPLv3",
    url='https://github.com/exponential-ventures/stripping',
    packages=find_packages(exclude=['*tests*', 'test*']),
    platforms=['any'],
    classifiers=[
        'License :: OSI Approved :: GNU LGPLv3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],

)
