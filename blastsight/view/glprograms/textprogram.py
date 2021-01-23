#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from OpenGL.GL import *
from .shaderprogram import ShaderProgram


class TextProgram(ShaderProgram):
    def __init__(self):
        super().__init__()
        self.base_name = 'Text'

    def draw(self) -> None:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glDepthMask(GL_FALSE)
        glEnable(GL_CULL_FACE)

        for gl_cull in [GL_FRONT, GL_BACK]:
            glCullFace(gl_cull)
            super().draw()

        glDisable(GL_CULL_FACE)
        glDepthMask(GL_TRUE)
