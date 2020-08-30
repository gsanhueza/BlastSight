#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .shaderprogram import ShaderProgram
from OpenGL.GL import *


class WireProgram(ShaderProgram):
    def __init__(self):
        super().__init__()
        self.base_name = 'Wireframe'

    def inner_draw(self, drawables: list) -> None:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        super().inner_draw(drawables)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
