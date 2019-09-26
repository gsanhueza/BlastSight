#!/usr/bin/env python

from .glcollection import GLCollection

from .backgroundgl import BackgroundGL
from .axisgl import AxisGL

from .glprograms.backgroundprogram import BackgroundProgram
from .glprograms.axisprogram import AxisProgram


class GLConstantCollection(GLCollection):
    def __init__(self, widget=None):
        super().__init__()
        self.programs[BackgroundProgram(widget)] = lambda: self.filter(BackgroundGL)
        self.programs[AxisProgram(widget)] = lambda: self.filter(AxisGL)
