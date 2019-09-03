#!/usr/bin/env python

from .shaderprogram import ShaderProgram
from OpenGL.GL import *


class MeshProgram(ShaderProgram):
    def __init__(self, widget):
        super().__init__(widget)
        self.base_name = 'Mesh'

    def draw(self):
        wireframed = []
        highlighted = []
        normal_opaque = []
        normal_transparent = []

        # Prepare meshes
        for drawable in self.drawables:
            if drawable.wireframe_enabled:
                wireframed.append(drawable)
            else:
                if drawable.element.alpha >= 0.99:
                    normal_opaque.append(drawable)
                else:
                    normal_transparent.append(drawable)
                if drawable.is_highlighted:
                    highlighted.append(drawable)

        # Wireframe
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        for drawable in wireframed:
            drawable.draw()

        # Highlighted
        glLineWidth(3)
        for drawable in highlighted:
            drawable.draw()
        glLineWidth(1)

        # Opaque/Normal
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        for drawable in normal_opaque:
            drawable.draw()

        # Transparent/Normal
        glDepthMask(GL_FALSE)
        glEnable(GL_CULL_FACE)

        for gl_cull in [GL_FRONT, GL_BACK]:
            glCullFace(gl_cull)
            for drawable in normal_transparent:
                drawable.draw()

        glDisable(GL_CULL_FACE)
        glDepthMask(GL_TRUE)
