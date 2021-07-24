#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .glcollection import GLCollection

from ..drawables.axisgl import AxisGL
from ..drawables.gridgl import GridGL

from ..glprograms.axisprogram import AxisProgram
from ..glprograms.gridcomposite import GridComposite


class GLPostCollection(GLCollection):
    def generate_associations(self):
        # Axis
        self.associate(AxisProgram(), AxisGL)

        # Grid
        self.associate(GridComposite(), GridGL)
