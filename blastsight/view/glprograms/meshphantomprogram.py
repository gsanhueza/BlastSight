#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from OpenGL.GL import *
from .meshprogram import ShaderProgram


class MeshPhantomProgram(ShaderProgram):
    def __init__(self):
        super().__init__()
        self.base_name = 'MeshPhantom'

    def inner_draw(self, drawables: list) -> None:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glDepthMask(GL_FALSE)
        glEnable(GL_CULL_FACE)

        for gl_cull in [GL_FRONT, GL_BACK]:
            glCullFace(gl_cull)
            super().inner_draw(drawables)

        glDisable(GL_CULL_FACE)
        glDepthMask(GL_TRUE)
