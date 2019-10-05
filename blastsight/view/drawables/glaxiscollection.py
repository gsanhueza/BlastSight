#!/usr/bin/env python

from .glcollection import GLCollection

from .axisgl import AxisGL
from .glprograms.axisprogram import AxisProgram


class GLAxisCollection(GLCollection):
    def __init__(self, widget=None):
        super().__init__()
        self.programs[AxisProgram(widget)] = lambda: self.filter(AxisGL)
