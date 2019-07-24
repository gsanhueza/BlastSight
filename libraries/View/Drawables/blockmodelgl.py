#!/usr/bin/env python

import numpy as np

from .gldrawable import GLDrawable
from OpenGL.GL import *


class BlockModelGL(GLDrawable):
    def __init__(self, widget=None, element=None):
        super().__init__(widget, element)

        # Sizes
        self.values_size = 0
        self.block_size = [1.0, 1.0, 1.0]
        self.min_val = 0.0
        self.max_val = 1.0

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1

        if self.vao is None:
            self.vao = glGenVertexArrays(1)

        self.vbos = glGenBuffers(2)

        # Data
        vertices = self.element.vertices
        values = self.element.values

        self.values_size = values.size
        self.min_val = values.min() if values.size > 0 else 0.0
        self.max_val = values.max() if values.size > 0 else 1.0
        self.block_size = self.element.block_size

        self.widget.makeCurrent()
        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbos[0])
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * vertices.size, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbos[1])
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * values.size, values, GL_STATIC_DRAW)
        glVertexAttribPointer(_COLOR, 1, GL_FLOAT, False, 0, None)

        glEnableVertexAttribArray(_POSITION)
        glEnableVertexAttribArray(_COLOR)

        glBindVertexArray(0)

    def draw(self):
        super().draw()
        if not self.is_visible:
            return

        glBindVertexArray(self.vao)
        # np.array([[0, 1, 2]], type) has size 3, despite having only 1 list there
        glDrawArrays(GL_POINTS, 0, self.values_size)
        glBindVertexArray(0)
