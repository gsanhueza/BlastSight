#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np

from .gldrawable import GLDrawable
from OpenGL.GL import *


class AxisGL(GLDrawable):
    def __init__(self, element=None, *args, **kwargs):
        super().__init__(element, *args, **kwargs)

    def generate_buffers(self) -> None:
        self._vaos = [glGenVertexArrays(1)]
        self._vbos = glGenBuffers(2)

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1

        # Data
        vertices = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0],
                             [0.0, 0.0, 0.0], [0.0, 1.0, 0.0],
                             [0.0, 0.0, 0.0], [0.0, 0.0, 1.0]]).astype(np.float32)

        colors = np.array([[1.0, 0.0, 0.0], [1.0, 0.0, 0.0],
                           [0.0, 1.0, 0.0], [0.0, 1.0, 0.0],
                           [0.0, 0.0, 1.0], [0.0, 0.0, 1.0]]).astype(np.float32)

        glBindVertexArray(self.vao)

        # Fill buffers (see GLDrawable)
        self.fill_buffer(_POSITION, 3, vertices, GLfloat, GL_FLOAT, self._vbos[_POSITION])
        self.fill_buffer(_COLOR, 3, colors, GLfloat, GL_FLOAT, self._vbos[_COLOR])

        glBindVertexArray(0)

    def draw(self) -> None:
        glDisable(GL_DEPTH_TEST)
        glBindVertexArray(self.vao)
        glLineWidth(5)
        glDrawArrays(GL_LINES, 0, 6)
        glLineWidth(1)
        glBindVertexArray(0)
        glEnable(GL_DEPTH_TEST)
