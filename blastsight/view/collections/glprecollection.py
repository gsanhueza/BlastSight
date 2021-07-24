#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .glcollection import GLCollection

from ..drawables.backgroundgl import BackgroundGL
from ..glprograms.backgroundprogram import BackgroundProgram


class GLPreCollection(GLCollection):
    def generate_associations(self):
        self.associate(BackgroundProgram(), BackgroundGL)
