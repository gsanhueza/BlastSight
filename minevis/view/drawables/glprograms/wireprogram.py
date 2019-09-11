#!/usr/bin/env python

from .shaderprogram import ShaderProgram
from OpenGL.GL import *


class WireProgram(ShaderProgram):
    def __init__(self, widget):
        super().__init__(widget)
        self.base_name = 'Wireframe'

    def draw(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        for drawable in self.drawables:
            drawable.draw()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
