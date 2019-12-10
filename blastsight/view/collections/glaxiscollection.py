#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .glcollection import GLCollection

from ..drawables.axisgl import AxisGL
from ..glprograms.axisprogram import AxisProgram


class GLAxisCollection(GLCollection):
    def __init__(self, widget=None):
        super().__init__()
        self.programs[AxisProgram(widget)] = lambda: self.filter(AxisGL)
