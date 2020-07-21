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


class SingletonDecorator:
    def __init__(self, klass):
        self.klass = klass
        self.existing_args = None
        self.existing_kwargs = None
        self.instance = None

    def __call__(self, *args, **kwargs):

        if self.instance is None:
            self.existing_args = args
            self.existing_kwargs = kwargs
            self.instance = self.klass(*args, **kwargs)

        else:

            # If the signature changes then the Singleton changes as well
            if args != self.existing_args or kwargs != self.existing_kwargs:
                self.existing_args = args
                self.existing_kwargs = kwargs
                self.instance = self.klass(*args, **kwargs)

        return self.instance
