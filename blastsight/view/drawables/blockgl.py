#!/usr/bin/env python

import numpy as np

from .gldrawable import GLDrawable
from OpenGL.GL import *


class BlockGL(GLDrawable):
    def __init__(self, element, *args, **kwargs):
        super().__init__(element, *args, **kwargs)
        self.num_cubes = 0

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1
        _ALPHA = 2

        # Generate VAO and VBOs (see GLDrawable)
        self.create_vao_vbos(3)

        # Data
        vertices = np.array(self.element.vertices, np.float32)
        colors = np.array(self.element.color, np.float32)
        alpha = np.array([self.element.alpha], np.float32)

        self.num_cubes = vertices.size // 3

        glBindVertexArray(self.vao)

        # buffer_properties = [(pointer, basesize, array, glsize, gltype)]
        buffer_properties = [(_POSITION, 3, vertices, GLfloat, GL_FLOAT),
                             (_COLOR, 3, colors, GLfloat, GL_FLOAT),
                             (_ALPHA, 1, alpha, GLfloat, GL_FLOAT),
                             ]

        # Fill buffers (see GLDrawable)
        self.fill_buffers(buffer_properties, self.vbos)

        # The attribute advances once per divisor instances of the set(s) of vertices being rendered
        # And guess what, we have just 1 instance, exactly what we wanted!
        glVertexAttribDivisor(_ALPHA, 1)

        glBindVertexArray(0)

    def draw(self):
        if not self.is_visible:
            return

        glBindVertexArray(self.vao)
        glDrawArrays(GL_POINTS, 0, self.num_cubes)
        glBindVertexArray(0)
