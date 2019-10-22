#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np

from .gldrawable import GLDrawable
from OpenGL.GL import *


class LineGL(GLDrawable):
    def __init__(self, element, *args, **kwargs):
        super().__init__(element, *args, **kwargs)

        self.vertices_size = 0

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1

        # Generate VAO and VBOs (see GLDrawable)
        self.create_vao_vbos(2)

        # Data
        vertices = self.element.vertices.astype(np.float32)
        colors = self.element.rgba.astype(np.float32)

        # np.array([[0, 1, 2]], type) has size 3, despite having only 1 list there
        self.vertices_size = vertices.size // 3

        glBindVertexArray(self.vao)

        # buffer_properties = [(pointer, basesize, array, glsize, gltype)]
        buffer_properties = [(_POSITION, 3, vertices, GLfloat, GL_FLOAT),
                             (_COLOR, 4, colors, GLfloat, GL_FLOAT),
                             ]

        # Fill buffers (see GLDrawable)
        self.fill_buffers(buffer_properties, self.vbos)
        glVertexAttribDivisor(_COLOR, 1)

        glBindVertexArray(0)

    def draw(self):
        glBindVertexArray(self.vao)
        glDrawArrays(GL_LINE_STRIP, 0, self.vertices_size)
        glBindVertexArray(0)
