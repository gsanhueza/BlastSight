#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
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
        self._legacy = kwargs.pop('legacy', False)

    """
    Properties
    """
    @property
    def is_legacy(self) -> bool:
        return self._legacy

    @is_legacy.setter
    def is_legacy(self, status: bool) -> None:
        self._legacy = status
        self.is_initialized = False
        self.notify()

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1
        _ALPHA = 2
        _TEMPLATE = 3

        # Generate VAO and VBOs (see GLDrawable)
        self.create_vao_vbos(4)

        # Data
        vertices = np.array(self.element.vertices, np.float32)
        colors = np.array(self.element.color, np.float32)
        alpha = np.array([self.element.alpha], np.float32)
        template = self.generate_cube(self.element.block_size)

        self.num_cubes = vertices.size // 3

        glBindVertexArray(self.vao)

        # buffer_properties = [(pointer, basesize, array, glsize, gltype)]
        buffer_properties = [(_POSITION, 3, vertices, GLfloat, GL_FLOAT),
                             (_COLOR, 3, colors, GLfloat, GL_FLOAT),
                             (_ALPHA, 1, alpha, GLfloat, GL_FLOAT),
                             (_TEMPLATE, 3, template, GLfloat, GL_FLOAT),
                             ]

        # Fill buffers (see GLDrawable)
        self.fill_buffers(buffer_properties, self.vbos)

        # The attribute advances once per divisor instances of the set(s) of vertices being rendered.
        if self.is_legacy:
            glVertexAttribDivisor(_POSITION, 1)
            glVertexAttribDivisor(_COLOR, 1)
        else:
            glVertexAttribDivisor(_POSITION, 0)
            glVertexAttribDivisor(_COLOR, 0)

        glVertexAttribDivisor(_TEMPLATE, 0)
        glVertexAttribDivisor(_ALPHA, -1)

        glBindVertexArray(0)

    def draw(self):
        # Force legacy method if OpenGL < 3.3
        if not self.is_legacy and float(f'{glGetIntegerv(GL_MAJOR_VERSION)}.{glGetIntegerv(GL_MINOR_VERSION)}') < 3.3:
            self.is_legacy = True
            return

        glBindVertexArray(self.vao)

        if self.is_legacy:
            glDrawArraysInstanced(GL_TRIANGLES, 0, 36, self.num_cubes)
        else:
            glDrawArrays(GL_POINTS, 0, self.num_cubes)

        glBindVertexArray(0)

    @staticmethod
    def generate_cube(size: np.ndarray) -> np.ndarray:
        vertices = np.array([
            [-1, -1, -1],
            [+1, -1, -1],
            [+1, +1, -1],
            [-1, +1, -1],
            [-1, -1, +1],
            [+1, -1, +1],
            [+1, +1, +1],
            [-1, +1, +1],
        ]) * size * 0.5

        indices = np.array([
            [1, 2, 3],
            [1, 3, 0],
            [4, 5, 6],
            [4, 6, 7],
            [0, 1, 5],
            [0, 5, 4],
            [2, 3, 7],
            [2, 7, 6],
            [3, 0, 4],
            [3, 4, 7],
            [1, 2, 6],
            [1, 6, 5],
        ])

        return vertices[indices].astype(np.float32)
