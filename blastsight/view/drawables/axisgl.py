#!/usr/bin/env python

#  Copyright (c) 2019-2023 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np

from .gldrawable import GLDrawable
from OpenGL.GL import *


class AxisGL(GLDrawable):
    def __init__(self, element=None, *args, **kwargs):
        super().__init__(element, *args, **kwargs)
        # With underscore to avoid overriding `element`
        self._vertices = np.array([]).astype(np.float32)
        self._colors = np.array([]).astype(np.float32)

    def generate_buffers(self) -> None:
        self._vaos = [glGenVertexArrays(1)]
        self._vbos = glGenBuffers(2)

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1

        # Data
        self._vertices = np.array([
            # X axis
            0.0, 0.0, 0.0,
            1.0, 0.0, 0.0,

            # Y axis
            0.0, 0.0, 0.0,
            0.0, 1.0, 0.0,

            # Z axis
            0.0, 0.0, 0.0,
            0.0, 0.0, 1.0,

            # Letter X
            1.1, 0.1, 0.0,
            1.3, -0.1, 0.0,
            1.1, -0.1, 0.0,
            1.3, 0.1, 0.0,

            # Letter Y
            -0.1, 1.3, 0.0,
            0.0, 1.2, 0.0,
            0.1, 1.3, 0.0,
            0.0, 1.2, 0.0,
            0.0, 1.1, 0.0,
            0.0, 1.2, 0.0,

            # Letter Z
            -0.1, 0.1, 1.1,
            0.1, 0.1, 1.1,
            0.1, 0.1, 1.1,
            -0.1, -0.1, 1.1,
            -0.1, -0.1, 1.1,
            0.1, -0.1, 1.1
        ]).astype(np.float32)

        self._colors = np.array([
            # Red
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            # Green
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            # Blue
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,

            # White: Letter X
            1.0, 1.0, 1.0,
            1.0, 1.0, 1.0,
            1.0, 1.0, 1.0,
            1.0, 1.0, 1.0,

            # White, Letter Y
            1.0, 1.0, 1.0,
            1.0, 1.0, 1.0,
            1.0, 1.0, 1.0,
            1.0, 1.0, 1.0,
            1.0, 1.0, 1.0,
            1.0, 1.0, 1.0,

            # White, Letter Z
            1.0, 1.0, 1.0,
            1.0, 1.0, 1.0,
            1.0, 1.0, 1.0,
            1.0, 1.0, 1.0,
            1.0, 1.0, 1.0,
            1.0, 1.0, 1.0
        ]).astype(np.float32)

        glBindVertexArray(self.vao)

        # Fill buffers (see GLDrawable)
        self.fill_buffer(_POSITION, 3, self._vertices, GLfloat, GL_FLOAT, self._vbos[_POSITION])
        self.fill_buffer(_COLOR, 3, self._colors, GLfloat, GL_FLOAT, self._vbos[_COLOR])

        glBindVertexArray(0)

    def draw(self) -> None:
        glDisable(GL_DEPTH_TEST)
        glBindVertexArray(self.vao)
        glLineWidth(3)
        glDrawArrays(GL_LINES, 0, self._vertices.size // 3)
        glLineWidth(1)
        glBindVertexArray(0)
        glEnable(GL_DEPTH_TEST)
