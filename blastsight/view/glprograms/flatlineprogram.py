#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from OpenGL.GL import *
from .shaderprogram import ShaderProgram


class FlatLineProgram(ShaderProgram):
    def __init__(self):
        super().__init__()
        self.base_name = 'FlatLine'

    def inner_draw(self, drawables: list) -> None:
        glDisable(GL_DEPTH_TEST)
        super().inner_draw(drawables)
        glEnable(GL_DEPTH_TEST)
