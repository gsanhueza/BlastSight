#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
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
        self._cross_sectionable = kwargs.pop('cross_section', False)

    """
    Properties
    """
    @property
    def is_standard(self) -> bool:
        return not self.is_legacy and not self.is_cross_sectionable

    @property
    def is_legacy(self) -> bool:
        return self._legacy

    @property
    def is_cross_sectionable(self) -> bool:
        return self._cross_sectionable

    @is_standard.setter
    def is_standard(self, status: bool) -> None:
        self._legacy = not status
        self.is_initialized = False
        self.notify()

    @is_legacy.setter
    def is_legacy(self, status: bool) -> None:
        self._legacy = status
        self.is_initialized = False
        self.notify()

    @is_cross_sectionable.setter
    def is_cross_sectionable(self, status: bool) -> None:
        self._cross_sectionable = status
        self.notify()

    """
    Internal methods
    """
    def generate_buffers(self) -> None:
        self._vaos = [glGenVertexArrays(1)]
        self._vbos = glGenBuffers(4)

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1
        _ALPHA = 2
        _TEMPLATE = 3

        # Data
        vertices = (self.element.vertices + self.rendering_offset).astype(np.float32)
        colors = np.array(self.element.color, np.float32)
        alpha = np.array([self.element.alpha], np.float32)
        template = self.generate_cube(self.element.block_size)

        self.num_cubes = len(vertices)

        glBindVertexArray(self.vao)

        # Fill buffers (see GLDrawable)
        self.fill_buffer(_POSITION, 3, vertices, GLfloat, GL_FLOAT, self._vbos[_POSITION])
        self.fill_buffer(_COLOR, 3, colors, GLfloat, GL_FLOAT, self._vbos[_COLOR])
        self.fill_buffer(_ALPHA, 1, alpha, GLfloat, GL_FLOAT, self._vbos[_ALPHA])
        self.fill_buffer(_TEMPLATE, 3, template, GLfloat, GL_FLOAT, self._vbos[_TEMPLATE])

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

    def draw(self) -> None:
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
