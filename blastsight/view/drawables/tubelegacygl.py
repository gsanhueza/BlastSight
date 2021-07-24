#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np

from .gldrawable import GLDrawable
from OpenGL.GL import *


class TubeLegacyGL(GLDrawable):
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
        vertices, indices = self.element.as_mesh()
        vertices = vertices[indices.astype(np.uint32)].astype(np.float32)
        self.num_vertices = vertices.size

        # Color extraction
        colors = []
        num_tubes = len(self.element.vertices) - 1
        triangles_per_tube = self.num_vertices // (3 * num_tubes)

        # Check if single-color (replicate) or multiple color (for each tube)
        if hasattr(self.element.color[0], '__len__'):
            for i in range(num_tubes):
                # When loop=True, we will replicate the last tube color
                index = min(i, len(self.element.color) - 1)
                base_color = np.append(self.element.color[index], self.element.alpha)
                colors.append(np.tile(base_color, triangles_per_tube))
        else:
            base_color = np.append(self.element.color, self.element.alpha)
            colors = np.tile(base_color, self.num_vertices)

        colors = np.array(colors, np.float32)

        glBindVertexArray(self.vao)

        # Fill buffers (see GLDrawable)
        self.fill_buffer(_POSITION, 3, vertices, GLfloat, GL_FLOAT, self._vbos[_POSITION])
        self.fill_buffer(_COLOR, 4, colors, GLfloat, GL_FLOAT, self._vbos[_COLOR])

        glBindBuffer(GL_ARRAY_BUFFER, self._vbos[-1])

        glBindVertexArray(0)

    def draw(self) -> None:
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, self.num_vertices)
        glBindVertexArray(0)
