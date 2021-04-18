#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np

from .gldrawable import GLDrawable
from OpenGL.GL import *


class GridGL(GLDrawable):
    def __init__(self, element=None, *args, **kwargs):
        super().__init__(element, *args, **kwargs)
        self.origin = kwargs.get('origin', np.zeros(3))
        self.lengths = kwargs.get('lengths', np.ones(3))
        self.color = kwargs.get('color', np.ones(3))

        self._total_lines = 0
        self._mark_separation = kwargs.get('mark_separation', 5)

    @property
    def x_pos(self) -> np.array:
        return self.origin + [self.lengths[0], 0.0, 0.0]

    @property
    def y_pos(self) -> np.array:
        return self.origin + [0.0, self.lengths[1], 0.0]

    @property
    def z_pos(self) -> np.array:
        return self.origin + [0.0, 0.0, self.lengths[2]]

    @property
    def bounding_box(self) -> tuple:
        # The bounding_box property is part of Element, but NullElement doesn't have it
        return self.origin, self.origin + self.lengths

    @property
    def mark_separation(self) -> int:
        return self._mark_separation

    @mark_separation.setter
    def mark_separation(self, value: int) -> None:
        self._mark_separation = int(value)
        self.reload()

    """
    Internal methods
    """
    def generate_buffers(self) -> None:
        self._vaos = [glGenVertexArrays(1)]
        self._vbos = glGenBuffers(2)

    def _xy_grid(self) -> list:
        rate = self.mark_separation
        response = []

        # Marks in X
        for shift_x in range(rate, int(self.lengths[0]), rate):
            response.append(self.origin + [shift_x, 0.0, 0.0])
            response.append(self.origin + [shift_x, self.lengths[1], 0.0])

        # Marks in Y
        for shift_y in range(rate, int(self.lengths[1]), rate):
            response.append(self.origin + [0.0, shift_y, 0.0])
            response.append(self.origin + [self.lengths[0], shift_y, 0.0])

        return response

    def _yz_grid(self) -> list:
        rate = self.mark_separation
        response = []

        # Marks in Y
        for shift_y in range(rate, int(self.lengths[1]), rate):
            response.append(self.origin + [0.0, shift_y, 0.0])
            response.append(self.origin + [0.0, shift_y, self.lengths[2]])

        # Marks in Z
        for shift_z in range(rate, int(self.lengths[2]), rate):
            response.append(self.origin + [0.0, 0.0, shift_z])
            response.append(self.origin + [0.0, self.lengths[1], shift_z])

        return response

    def _xz_grid(self) -> list:
        rate = self.mark_separation
        response = []

        # Marks in Z
        for shift_z in range(rate, int(self.lengths[2]), rate):
            response.append(self.origin + [0.0, 0.0, shift_z])
            response.append(self.origin + [self.lengths[0], 0.0, shift_z])

        # Marks in X
        for shift_x in range(rate, int(self.lengths[0]), rate):
            response.append(self.origin + [shift_x, 0.0, 0.0])
            response.append(self.origin + [shift_x, 0.0, self.lengths[2]])

        return response

    def _x_mark(self, shift: int, mark_size) -> list:
        return [
            self.origin + [shift, -mark_size, 0.0],
            self.origin + [shift, +mark_size, 0.0],
        ]

    def _y_mark(self, shift: int, mark_size) -> list:
        return [
            self.origin + [-mark_size, shift, 0.0],
            self.origin + [+mark_size, shift, 0.0],
        ]

    def _z_mark(self, shift: int, mark_size) -> list:
        return [
            self.origin + [-mark_size, 0.0, shift],
            self.origin + [+mark_size, 0.0, shift],
        ]

    def generate_marks(self, mark_size: float = 1.0) -> np.ndarray:
        marks = []
        rate = self.mark_separation

        # Marks in X
        for i in range(rate, int(self.lengths[0]), rate):
            marks += self._x_mark(i, mark_size)

        # Marks in Y
        for i in range(rate, int(self.lengths[1]), rate):
            marks += self._y_mark(i, mark_size)

        # Marks in Z
        for i in range(rate, int(self.lengths[2]), rate):
            marks += self._z_mark(i, mark_size)

        return np.array(marks).reshape((-1, 3)).astype(np.float32)

    def generate_grid(self) -> np.ndarray:
        marks = []

        # Grid
        marks += self._xy_grid()
        marks += self._yz_grid()
        marks += self._xz_grid()

        return np.array(marks).reshape((-1, 3)).astype(np.float32)

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1

        # Data
        vertices = np.array([self.origin, self.x_pos,
                             self.origin, self.y_pos,
                             self.origin, self.z_pos]).astype(np.float32)

        marks = self.generate_grid()
        vertices = np.concatenate((vertices, marks), axis=0).astype(np.float32)

        # Offset
        vertices = (vertices + self.rendering_offset).astype(np.float32)

        self._total_lines = len(vertices)

        # Color
        colors = np.tile(self.color, self._total_lines).astype(np.float32)

        glBindVertexArray(self.vao)

        # Fill buffers (see GLDrawable)
        self.fill_buffer(_POSITION, 3, vertices, GLfloat, GL_FLOAT, self._vbos[_POSITION])
        self.fill_buffer(_COLOR, 3, colors, GLfloat, GL_FLOAT, self._vbos[_COLOR])

        glBindVertexArray(0)

    def draw(self) -> None:
        glBindVertexArray(self.vao)
        glLineWidth(3)
        glDrawArrays(GL_LINES, 0, self._total_lines)
        glLineWidth(1)
        glBindVertexArray(0)
