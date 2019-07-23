#!/usr/bin/env python

import numpy as np

from .gldrawable import GLDrawable
from OpenGL.GL import *


class AxisGL(GLDrawable):
    def __init__(self, widget=None, element=None):
        super().__init__(widget, element)

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1

        self.vao = glGenVertexArrays(1)
        self.vbos = glGenBuffers(2)

        # Data
        vertices = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0],
                             [0.0, 0.0, 0.0], [0.0, 1.0, 0.0],
                             [0.0, 0.0, 0.0], [0.0, 0.0, 1.0]], np.float32)

        colors = np.array([[1.0, 0.0, 0.0], [1.0, 0.0, 0.0],
                           [0.0, 1.0, 0.0], [0.0, 1.0, 0.0],
                           [0.0, 0.0, 1.0], [0.0, 0.0, 1.0]], np.float32)

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbos[0])
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * vertices.size, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbos[1])
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * colors.size, colors, GL_STATIC_DRAW)
        glVertexAttribPointer(_COLOR, 3, GL_FLOAT, False, 0, None)

        glEnableVertexAttribArray(_POSITION)
        glEnableVertexAttribArray(_COLOR)

        glBindVertexArray(0)

    def draw(self):
        super().draw()
        if not self.is_visible:
            return

        glBindVertexArray(self.vao)
        glDrawArrays(GL_LINES, 0, 18)
        glBindVertexArray(0)
