#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np

from .gldrawable import GLDrawable
from OpenGL.GL import *


class AxisGL(GLDrawable):
    def __init__(self, element=None, *args, **kwargs):
        super().__init__(element, *args, **kwargs)

    def __dir__(self):
        return sorted(set(dir(type(self)) + list(self.__dict__.keys())))

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1

        # Generate VAO and VBOs (see GLDrawable)
        self.create_vao_vbos(2)

        # Data
        vertices = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0],
                             [0.0, 0.0, 0.0], [0.0, 1.0, 0.0],
                             [0.0, 0.0, 0.0], [0.0, 0.0, 1.0]]).astype(np.float32)

        colors = np.array([[1.0, 0.0, 0.0], [1.0, 0.0, 0.0],
                           [0.0, 1.0, 0.0], [0.0, 1.0, 0.0],
                           [0.0, 0.0, 1.0], [0.0, 0.0, 1.0]]).astype(np.float32)

        glBindVertexArray(self.vao)

        # buffer_properties = [(pointer, basesize, array, glsize, gltype)]
        buffer_properties = [(_POSITION, 3, vertices, GLfloat, GL_FLOAT),
                             (_COLOR, 3, colors, GLfloat, GL_FLOAT),
                             ]

        # Fill buffers (see GLDrawable)
        self.fill_buffers(buffer_properties, self.vbos)

        glBindVertexArray(0)

    def draw(self):
        glDisable(GL_DEPTH_TEST)
        glBindVertexArray(self.vao)
        glLineWidth(5)
        glDrawArrays(GL_LINES, 0, 18)
        glLineWidth(1)
        glBindVertexArray(0)
        glEnable(GL_DEPTH_TEST)
