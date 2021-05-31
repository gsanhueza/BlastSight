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
        self._origin = kwargs.get('origin', np.zeros(3))
        self._size = kwargs.get('size', 10 * np.ones(3))
        self._color = kwargs.get('color', np.array([1.0, 0.8, 0.0]))
        self.mark_separation = kwargs.get('mark_separation', 1)
        self.total_lines = 0

    @property
    def origin(self) -> np.array:
        return self._origin

    @origin.setter
    def origin(self, value: iter) -> None:
        self._origin = np.array(value, np.float32)

    @property
    def size(self) -> np.array:
        return self._size

    @size.setter
    def size(self, value: iter) -> None:
        self._size = np.array(value, np.int32)

    @property
    def color(self) -> np.array:
        return self._color

    @color.setter
    def color(self, value: iter) -> None:
        self._color = np.array(value, np.float32)

    """
    Utilities
    """
    @property
    def x_pos(self) -> np.array:
        return self.origin + [self.size[0], 0.0, 0.0]

    @property
    def y_pos(self) -> np.array:
        return self.origin + [0.0, self.size[1], 0.0]

    @property
    def z_pos(self) -> np.array:
        return self.origin + [0.0, 0.0, self.size[2]]

    @property
    def x_divisions(self) -> np.ndarray:
        return np.ceil(np.arange(self.origin[0], self.x_pos[0], self.mark_separation)) - self.origin[0]

    @property
    def y_divisions(self) -> np.ndarray:
        return np.ceil(np.arange(self.origin[1], self.y_pos[1], self.mark_separation)) - self.origin[1]

    @property
    def z_divisions(self) -> np.ndarray:
        return np.ceil(np.arange(self.origin[2], self.z_pos[2], self.mark_separation)) - self.origin[2]

    @property
    def bounding_box(self) -> tuple:
        # The bounding_box property is part of Element, but NullElement doesn't have it
        return self.origin, self.origin + self.size

    """
    Internal methods
    """
    def generate_buffers(self) -> None:
        self._vaos = [glGenVertexArrays(1)]
        self._vbos = glGenBuffers(2)

    def _xy_grid(self) -> list:
        response = []

        # Lines in X
        for x_div in self.x_divisions:
            response.append(self.origin + [x_div, 0.0, 0.0])
            response.append(self.origin + [x_div, self.size[1], 0.0])

        # Lines in Y
        for y_div in self.y_divisions:
            response.append(self.origin + [0.0, y_div, 0.0])
            response.append(self.origin + [self.size[0], y_div, 0.0])

        return response

    def _yz_grid(self) -> list:
        response = []

        # Lines in Y
        for y_div in self.y_divisions:
            response.append(self.origin + [0.0, y_div, 0.0])
            response.append(self.origin + [0.0, y_div, self.size[2]])

        # Lines in Z
        for z_div in self.z_divisions:
            response.append(self.origin + [0.0, 0.0, z_div])
            response.append(self.origin + [0.0, self.size[1], z_div])

        return response

    def _xz_grid(self) -> list:
        response = []

        # Lines in X
        for x_div in self.x_divisions:
            response.append(self.origin + [x_div, 0.0, 0.0])
            response.append(self.origin + [x_div, 0.0, self.size[2]])

        # Lines in Z
        for z_div in self.z_divisions:
            response.append(self.origin + [0.0, 0.0, z_div])
            response.append(self.origin + [self.size[0], 0.0, z_div])

        return response

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
        vertices = self.generate_grid().astype(np.float32)
        self.total_lines = len(vertices)

        # Color
        colors = np.tile(self.color, self.total_lines).astype(np.float32)

        glBindVertexArray(self.vao)

        # Fill buffers (see GLDrawable)
        self.fill_buffer(_POSITION, 3, vertices, GLfloat, GL_FLOAT, self._vbos[_POSITION])
        self.fill_buffer(_COLOR, 3, colors, GLfloat, GL_FLOAT, self._vbos[_COLOR])

        glBindVertexArray(0)

    def draw(self) -> None:
        glBindVertexArray(self.vao)
        glLineWidth(3)
        glDrawArrays(GL_LINES, 0, self.total_lines)
        glLineWidth(1)
        glBindVertexArray(0)
