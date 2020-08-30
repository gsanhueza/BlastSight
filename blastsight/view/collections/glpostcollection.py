#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .glcollection import GLCollection

from ..drawables.axisgl import AxisGL
from ..glprograms.axisprogram import AxisProgram


class GLPostCollection(GLCollection):
    def __init__(self):
        super().__init__()
        self.associate(AxisProgram(), AxisGL)
