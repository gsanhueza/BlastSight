#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np

from .gldrawable import GLDrawable
from OpenGL.GL import *


class BlockGL(GLDrawable):
    def __init__(self, element, *args, **kwargs):
        super().__init__(element, *args, **kwargs)
        self.num_cubes = 0

    @property
    def is_standard(self) -> bool:
        return not self.is_cross_sectioned

    """
    Internal methods
    """
    def generate_buffers(self) -> None:
        self._vaos = [glGenVertexArrays(1)]
        self._vbos = glGenBuffers(3)

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1
        _ALPHA = 2

        # Data
        vertices = self.element.vertices.astype(np.float32)
        colors = np.array(self.element.color, np.float32)
        alpha = np.array([self.element.alpha], np.float32)

        self.num_cubes = len(vertices)

        glBindVertexArray(self.vao)

        # Fill buffers (see GLDrawable)
        self.fill_buffer(_POSITION, 3, vertices, GLfloat, GL_FLOAT, self._vbos[_POSITION])
        self.fill_buffer(_COLOR, 3, colors, GLfloat, GL_FLOAT, self._vbos[_COLOR])
        self.fill_buffer(_ALPHA, 1, alpha, GLfloat, GL_FLOAT, self._vbos[_ALPHA])

        # The attribute advances once per divisor instances of the set(s) of vertices being rendered.
        glVertexAttribDivisor(_ALPHA, 1)

        glBindVertexArray(0)

    def draw(self) -> None:
        glBindVertexArray(self.vao)
        glDrawArrays(GL_POINTS, 0, self.num_cubes)
        glBindVertexArray(0)
