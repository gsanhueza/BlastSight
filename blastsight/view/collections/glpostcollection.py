#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .glcollection import GLCollection

from ..drawables.axisgl import AxisGL
from ..drawables.textgl import TextGL
from ..glprograms.axisprogram import AxisProgram
from ..glprograms.textprogram import TextProgram


class GLPostCollection(GLCollection):
    def __init__(self):
        super().__init__()
        self.associate(AxisProgram(), AxisGL)
        self.associate(TextProgram(), TextGL)
