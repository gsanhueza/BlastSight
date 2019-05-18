#!/usr/bin/env python

from Model.model import Model


def Singleton(klass):
    if not klass._instance:
        klass._instance = klass()

    return klass._instance


model_handler = Singleton(Model)
