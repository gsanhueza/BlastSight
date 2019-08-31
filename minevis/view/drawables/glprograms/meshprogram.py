#!/usr/bin/env python

from .shaderprogram import ShaderProgram
from OpenGL.GL import *


class MeshProgram(ShaderProgram):
    def __init__(self, widget):
        super().__init__(widget)
        self.base_name = 'Mesh'

    def draw(self):
        wireframed = []
        normal_opaque = []
        normal_glass = []

        # Prepare meshes
        for drawable in self.drawables:
            if drawable.wireframe_enabled:
                wireframed.append(drawable)
            else:
                if drawable.element.alpha >= 0.99:
                    normal_opaque.append(drawable)
                else:
                    normal_glass.append(drawable)

        # Wireframe
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        for drawable in wireframed:
            drawable.draw()

        # Opaque/Normal
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        for drawable in normal_opaque:
            drawable.draw()

        # Transparent/Normal
        for drawable in normal_glass:
            drawable.draw()
