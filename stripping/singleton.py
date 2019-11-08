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
