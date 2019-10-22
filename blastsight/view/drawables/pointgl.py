#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np

from .gldrawable import GLDrawable
from OpenGL.GL import *


class PointGL(GLDrawable):
    def __init__(self, element, *args, **kwargs):
        super().__init__(element, *args, **kwargs)
        self.num_points = 0

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1
        _ALPHA = 2
        _SIZE = 3

        # Generate VAO and VBOs (see GLDrawable)
        self.create_vao_vbos(4)

        # Data
        vertices = self.element.vertices.astype(np.float32)
        colors = self.element.color.astype(np.float32)
        alpha = np.array([self.element.alpha], np.float32)
        sizes = self.element.point_size.astype(np.float32)

        self.num_points = sizes.size

        glBindVertexArray(self.vao)

        # buffer_properties = [(pointer, basesize, array, glsize, gltype)]
        buffer_properties = [(_POSITION, 3, vertices, GLfloat, GL_FLOAT),
                             (_COLOR, 3, colors, GLfloat, GL_FLOAT),
                             (_ALPHA, 1, alpha, GLfloat, GL_FLOAT),
                             (_SIZE, 1, sizes, GLfloat, GL_FLOAT),
                             ]

        # Fill buffers (see GLDrawable)
        self.fill_buffers(buffer_properties, self.vbos)

        # The attribute advances once per divisor instances of the set(s) of vertices being rendered
        # And guess what, we have just 1 instance, exactly what we wanted!
        glVertexAttribDivisor(_ALPHA, 1)

        glBindVertexArray(0)

    def draw(self):
        glBindVertexArray(self.vao)
        glDrawArrays(GL_POINTS, 0, self.num_points)
        glBindVertexArray(0)
