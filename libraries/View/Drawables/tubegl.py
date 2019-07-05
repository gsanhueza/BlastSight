#!/usr/bin/env python

import numpy as np

from .gldrawable import GLDrawable
from OpenGL.GL import *


class TubeGL(GLDrawable):
    def __init__(self, widget=None, element=None):
        super().__init__(widget, element)

        # Sizes
        self.vertices_size = 0
        self.vao = None

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1

        self.vao = glGenVertexArrays(1)

        # VBO
        vertices_vbo = glGenBuffers(1)
        color_vbo = glGenBuffers(1)

        # Data
        vertices = self.element.vertices
        self.vertices_size = vertices.size
        colors = np.array(np.tile(np.append(self.element.color, self.element.alpha),
                                  vertices.size // 3), np.float32)

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, vertices_vbo)
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * vertices.size, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None)

        glBindBuffer(GL_ARRAY_BUFFER, color_vbo)
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * colors.size, colors, GL_STATIC_DRAW)
        glVertexAttribPointer(_COLOR, 4, GL_FLOAT, False, 0, None)

        glEnableVertexAttribArray(_POSITION)
        glEnableVertexAttribArray(_COLOR)

        glBindVertexArray(0)

    def draw(self):
        super().draw()
        if not self.is_visible:
            return

        glBindVertexArray(self.vao)
        # np.array([[0, 1, 2]], type) has size 3, despite having only 1 list there
        glDrawArrays(GL_LINE_STRIP, 0, self.vertices_size)
