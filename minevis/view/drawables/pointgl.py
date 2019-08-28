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
        _ALPHA = 2
        _SIZE = 3

        if self.vao is None:
            self.vao = glGenVertexArrays(1)
            self.vbos = glGenBuffers(4)

        # Data
        vertices = self.element.vertices.astype(np.float32)
        colors = self.element.color.astype(np.float32)
        alpha = np.array([self.element.alpha], np.float32)
        sizes = self.element.point_size.astype(np.uint16)

        self.num_points = sizes.size

        self.widget.makeCurrent()
        glBindVertexArray(self.vao)

        # buffers = [(pointer, basesize, array, glsize, gltype)]
        buffers = [(_POSITION, 3, vertices, GLfloat, GL_FLOAT),
                   (_COLOR, 3, colors, GLfloat, GL_FLOAT),
                   (_ALPHA, 1, alpha, GLfloat, GL_FLOAT),
                   (_SIZE, 1, sizes, GLushort, GL_UNSIGNED_SHORT)  # Point size = [0, 65535]
                   ]

        for i, buf in enumerate(buffers):
            pointer, basesize, array, glsize, gltype = buf
            glBindBuffer(GL_ARRAY_BUFFER, self.vbos[i])
            glBufferData(GL_ARRAY_BUFFER, sizeof(glsize) * array.size, array, GL_STATIC_DRAW)
            glVertexAttribPointer(pointer, basesize, gltype, False, 0, None)
            glEnableVertexAttribArray(pointer)

        # The attribute advances once per divisor instances of the set(s) of vertices being rendered
        # And guess what, we have just 1 instance, exactly what we wanted!
        glVertexAttribDivisor(_ALPHA, 1)

        glBindVertexArray(0)

    def draw(self):
        super().draw()
        if not self.is_visible:
            return

        glBindVertexArray(self.vao)
        glDrawArrays(GL_POINTS, 0, self.num_points)
        glBindVertexArray(0)
