#!/usr/bin/env python

import numpy as np

from .gldrawable import GLDrawable
from OpenGL.GL import *


class MeshGL(GLDrawable):
    def __init__(self, widget=None, element=None):
        super().__init__(widget, element)

        # Size
        self.indices_size = 0
        self.vao = None

        # Wireframe
        self.wireframe_enabled = False

    def toggle_wireframe(self) -> bool:
        self.wireframe_enabled = not self.wireframe_enabled
        return self.wireframe_enabled

    def disable_wireframe(self) -> None:
        self.wireframe_enabled = False

    def enable_wireframe(self):
        self.wireframe_enabled = True

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1

        self.vao = glGenVertexArrays(1)

        # VBO
        vertices_vbo = glGenBuffers(1)
        indices_ebo = glGenBuffers(1)
        colors_vbo = glGenBuffers(1)

        # Data
        vertices = self.element.vertices
        indices = self.element.indices
        colors = np.array(np.tile(np.append(self.element.values, self.element.alpha),
                                  vertices.size // 3), np.float32)

        self.indices_size = indices.size

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, vertices_vbo)
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * vertices.size, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None)

        glBindBuffer(GL_ARRAY_BUFFER, colors_vbo)
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * colors.size, colors, GL_STATIC_DRAW)
        glVertexAttribPointer(_COLOR, 4, GL_FLOAT, False, 0, None)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indices_ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(_POSITION)
        glEnableVertexAttribArray(_COLOR)

        glBindVertexArray(0)

        del vertices
        del indices
        del colors

    def draw(self):
        super().draw()
        if not self.is_visible:
            return

        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.indices_size, GL_UNSIGNED_INT, None)
