#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .shaderprogram import ShaderProgram
from OpenGL.GL import *


class HighlightProgram(ShaderProgram):
    def __init__(self):
        super().__init__()
        self.base_name = 'Highlight'

    def inner_draw(self, drawables: list) -> None:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glLineWidth(3)
        super().inner_draw(drawables)
        glLineWidth(1)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
