#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .shaderprogram import ShaderProgram
from OpenGL.GL import *


class MeshProgram(ShaderProgram):
    def __init__(self, viewer):
        super().__init__(viewer)
        self.base_name = 'Mesh'

    def draw(self) -> None:
        # Highlighted
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glLineWidth(3)
        super().inner_draw(filter(lambda x: x.is_highlighted, self.opaques))
        glLineWidth(1)

        # Opaque
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        super().draw()

    def redraw(self) -> None:
        # Highlighted
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glLineWidth(3)
        super().inner_draw(filter(lambda x: x.is_highlighted, self.transparents))
        glLineWidth(1)

        # Transparent
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glDepthMask(GL_FALSE)
        glEnable(GL_CULL_FACE)

        for gl_cull in [GL_FRONT, GL_BACK]:
            glCullFace(gl_cull)
            super().redraw()

        glDisable(GL_CULL_FACE)
        glDepthMask(GL_TRUE)
