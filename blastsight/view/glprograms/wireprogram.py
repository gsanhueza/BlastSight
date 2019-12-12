#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .meshprogram import MeshProgram
from OpenGL.GL import *


class WireProgram(MeshProgram):
    def __init__(self, widget):
        super().__init__(widget)
        self.base_name = 'Wireframe'

    def draw(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        for drawable in self.drawables:
            drawable.draw()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def redraw(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        for drawable in self.transparents:
            drawable.draw()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
