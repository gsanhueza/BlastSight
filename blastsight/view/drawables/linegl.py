#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np

from .gldrawable import GLDrawable
from OpenGL.GL import *


class LineGL(GLDrawable):
    def __init__(self, element, *args, **kwargs):
        super().__init__(element, *args, **kwargs)
        self.num_vertices = 0

    def generate_buffers(self) -> None:
        self._vaos = [glGenVertexArrays(1)]
        self._vbos = glGenBuffers(2)

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1

        # Data
        vertices = self.element.vertices.astype(np.float32)
        colors = self.element.rgba.astype(np.float32)

        # np.array([[0, 1, 2]], type) has size 3, despite having only 1 list there
        self.num_vertices = len(vertices)

        glBindVertexArray(self.vao)

        # Fill buffers (see GLDrawable)
        self.fill_buffer(_POSITION, 3, vertices, GLfloat, GL_FLOAT, self._vbos[_POSITION])
        self.fill_buffer(_COLOR, 4, colors, GLfloat, GL_FLOAT, self._vbos[_COLOR])

        glVertexAttribDivisor(_COLOR, 1)

        glBindVertexArray(0)

    def draw(self) -> None:
        glBindVertexArray(self.vao)
        glLineWidth(self.element.thickness)
        glDrawArrays(GL_LINE_STRIP, 0, self.num_vertices)
        glLineWidth(1)
        glBindVertexArray(0)
