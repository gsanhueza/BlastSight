#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np

from .gldrawable import GLDrawable
from OpenGL.GL import *


class TubeGL(GLDrawable):
    def __init__(self, element, *args, **kwargs):
        super().__init__(element, *args, **kwargs)

        self.indices_size = 0

    def generate_buffers(self) -> None:
        self._vaos = [glGenVertexArrays(1)]
        self._vbos = glGenBuffers(3)

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1

        # Data
        vertices, indices = self.element.as_mesh()

        vertices = (vertices + self.rendering_offset).astype(np.float32)
        indices = np.array(indices).astype(np.uint32)
        colors = self.element.rgba.astype(np.float32)

        self.indices_size = indices.size

        glBindVertexArray(self.vao)

        # Fill buffers (see GLDrawable)
        self.fill_buffer(_POSITION, 3, vertices, GLfloat, GL_FLOAT, self._vbos[_POSITION])
        self.fill_buffer(_COLOR, 4, colors, GLfloat, GL_FLOAT, self._vbos[_COLOR])

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._vbos[-1])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

        # The attribute advances once per divisor instances of the set(s) of vertices being rendered
        # And guess what, we have just 1 instance, exactly what we wanted!
        glVertexAttribDivisor(_COLOR, 1)

        glBindVertexArray(0)

    def draw(self) -> None:
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.indices_size, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
