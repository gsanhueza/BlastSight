#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np

from .gldrawable import GLDrawable
from OpenGL.GL import *


class TubeGL(GLDrawable):
    def __init__(self, element, *args, **kwargs):
        super().__init__(element, *args, **kwargs)
        self.num_tubes = 0

    def generate_buffers(self) -> None:
        self._vaos = [glGenVertexArrays(1)]
        self._vbos = glGenBuffers(3)

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1
        _PROPERTIES = 2  # radius, resolution

        # Data
        vertices = self.element.vertices
        self.num_tubes = len(self.element.vertices)

        # Color extraction
        colors = []

        # Check if single-color (replicate) or multiple color (for each tube)
        if hasattr(self.element.color[0], '__len__'):
            for i in range(self.num_tubes):
                # When loop=True, we will replicate the last tube color
                index = min(i, len(self.element.color) - 1)
                base_color = np.append(self.element.color[index], self.element.alpha)
                colors.append(base_color)
        else:
            base_color = np.append(self.element.color, self.element.alpha)
            colors = np.tile(base_color, self.num_tubes)

        colors = np.array(colors, np.float32)

        # Radius/Resolution
        properties = np.array([self.element.radius, self.element.resolution], np.float32)

        glBindVertexArray(self.vao)

        # Fill buffers (see GLDrawable)
        self.fill_buffer(_POSITION, 3, vertices, GLfloat, GL_FLOAT, self._vbos[_POSITION])
        self.fill_buffer(_COLOR, 4, colors, GLfloat, GL_FLOAT, self._vbos[_COLOR])
        self.fill_buffer(_PROPERTIES, 2, properties, GLfloat, GL_FLOAT, self._vbos[_PROPERTIES])

        # Shared properties for all mini-tubes
        glVertexAttribDivisor(_PROPERTIES, 1)

        glBindBuffer(GL_ARRAY_BUFFER, self._vbos[-1])

        glBindVertexArray(0)

    def draw(self) -> None:
        glBindVertexArray(self.vao)
        glDrawArrays(GL_LINE_STRIP, 0, self.num_tubes)
        glBindVertexArray(0)
