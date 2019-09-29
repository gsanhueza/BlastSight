#!/usr/bin/env python

from .glcollection import GLCollection

from .backgroundgl import BackgroundGL
from .glprograms.backgroundprogram import BackgroundProgram


class GLBackgroundCollection(GLCollection):
    def __init__(self, widget=None):
        super().__init__()
        self.programs[BackgroundProgram(widget)] = lambda: self.filter(BackgroundGL)
