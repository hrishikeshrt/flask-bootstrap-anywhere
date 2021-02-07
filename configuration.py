#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Hrishikesh Terdalkar
"""

###############################################################################


class Configuration(dict):
    def __init__(self, obj={}):
        super().__init__(obj)

    def __dir__(self):
        return list(self)

    def __repr__(self):
        return "%s(%s)" % (type(self).__name__, super().__repr__())

    def __getattribute__(self, name, *args):
        try:
            return self[name]
        except KeyError:
            msg = "'%s' object has no attribute '%s'"
            raise AttributeError(msg % (type(self).__name__, name))

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]

    # ----------------------------------------------------------------------- #
    # static methods
    @staticmethod
    def hasattr(ns, name):
        try:
            object.__getattribute__(ns, name)
        except AttributeError:
            return False
        return True

    @staticmethod
    def getattr(ns, name):
        return object.__getattribute__(ns, name)

    @staticmethod
    def setattr(ns, name, value):
        return object.__setattr__(ns, name, value)

    @staticmethod
    def delattr(ns, name):
        return object.__delattr__(ns, name)

###############################################################################
