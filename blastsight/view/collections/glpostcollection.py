#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .glcollection import GLCollection

from ..drawables.axisgl import AxisGL
from ..glprograms.orientationaxisprogram import OrientationAxisProgram


class GLPostCollection(GLCollection):
    def generate_associations(self):
        self.associate(OrientationAxisProgram(), AxisGL)
