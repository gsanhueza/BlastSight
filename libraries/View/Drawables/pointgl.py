#!/usr/bin/env python

import numpy as np

from .gldrawable import GLDrawable
from OpenGL.GL import *


class PointGL(GLDrawable):
    def __init__(self, widget=None, element=None):
        super().__init__(widget, element)
        self.num_points = 0

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1
        _SIZE = 2

        if self.vao is None:
            self.vao = glGenVertexArrays(1)
            self.vbos = glGenBuffers(3)

        # Data
        vertices = self.element.vertices.astype(np.float32)
        colors = self.element.colors.astype(np.float32)
        sizes = self.element.point_size.astype(np.float32)

        print(f'Vertices: {vertices}')
        print(f'Colors: {colors}')
        print(f'Sizes: {sizes}')

        self.num_points = sizes.size

        self.widget.makeCurrent()
        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbos[0])
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * vertices.size, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbos[1])
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * colors.size, colors, GL_STATIC_DRAW)
        glVertexAttribPointer(_COLOR, 3, GL_FLOAT, False, 0, None)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbos[2])
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * sizes.size, sizes, GL_STATIC_DRAW)
        glVertexAttribPointer(_SIZE, 1, GL_FLOAT, False, 0, None)

        glEnableVertexAttribArray(_POSITION)
        glEnableVertexAttribArray(_COLOR)
        glEnableVertexAttribArray(_SIZE)

        glBindVertexArray(0)

        del vertices
        del colors
        del sizes

    def draw(self):
        super().draw()
        if not self.is_visible:
            return

        glBindVertexArray(self.vao)
        glDrawArrays(GL_POINTS, 0, self.num_points)
        glBindVertexArray(0)
