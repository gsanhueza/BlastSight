#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .shaderprogram import ShaderProgram
from OpenGL.GL import *


class MeshProgram(ShaderProgram):
    def __init__(self, widget):
        super().__init__(widget)
        self.base_name = 'Mesh'

    def draw(self):
        # Highlighted
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glLineWidth(3)
        for drawable in filter(lambda x: x.is_highlighted, self.drawables):
            drawable.draw()
        glLineWidth(1)

        # Opaque
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        for drawable in self.drawables:
            drawable.draw()

    def redraw(self):
        # Highlighted
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glLineWidth(3)
        for drawable in filter(lambda x: x.is_highlighted, self.transparents):
            drawable.draw()
        glLineWidth(1)

        # Transparent
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glDepthMask(GL_FALSE)
        glEnable(GL_CULL_FACE)

        for gl_cull in [GL_FRONT, GL_BACK]:
            glCullFace(gl_cull)
            for drawable in self.transparents:
                drawable.draw()

        glDisable(GL_CULL_FACE)
        glDepthMask(GL_TRUE)
