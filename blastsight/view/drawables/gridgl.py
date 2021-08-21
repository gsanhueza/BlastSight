#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np

from .gldrawable import GLDrawable
from OpenGL.GL import *


class GridGL(GLDrawable):
    def __init__(self, element=None, *args, **kwargs):
        super().__init__(element, *args, **kwargs)

        # Lines description
        self._origin = kwargs.get('origin', np.zeros(3))
        self._size = kwargs.get('size', 10 * np.ones(3))
        self._grid_color = kwargs.get('grid_color', np.array([1.0, 0.8, 0.0]))
        self._text_color = kwargs.get('text_color', np.array([1.0, 1.0, 1.0]))
        self.mark_separation = kwargs.get('mark_separation', 1)
        self.enclosed = kwargs.get('enclosed', True)
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
    def grid_color(self) -> np.array:
        return self._grid_color

    @grid_color.setter
    def grid_color(self, value: iter) -> None:
        self._grid_color = np.array(value, np.float32)

    @property
    def text_color(self) -> np.array:
        return self._text_color

    @text_color.setter
    def text_color(self, value: iter) -> None:
        self._text_color = np.array(value, np.float32)

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

    def generate_grid(self) -> np.ndarray:
        """
        Let the grid be

         (Z) ^
             | |
             | |  ^(Y)
             | | /
             | |/_______  <-- Example of a line in the "Y Corner".
             | /
             +/__________> (X)

        A line of the "X corner" is (x, 0, MAX_Z) -> (x, 0, 0) -> (x, MAX_Y, 0)
        A line of the "Y corner" is (0, y, MAX_Z) -> (0, y, 0) -> (MAX_X, y, 0)
        A line of the "Z corner" is (MAX_X, 0, z) -> (0, 0, z) -> (0, MAX_Y, z)
        """
        marks = []

        # Grid
        marks += self.x_corner()
        marks += self.y_corner()
        marks += self.z_corner()

        return np.array(marks).reshape((-1, 3)).astype(np.float32)

    def x_corner(self) -> list:
        # A line of the "X corner" is (x, 0, MAX_Z) -> (x, 0, 0) -> (x, MAX_Y, 0)
        response = []
        origin = self.origin
        divisions = self.x_divisions

        # Enclose the grid if required
        if self.enclosed:
            divisions = np.append(divisions, self.size[0])

        for x in divisions:
            response.append(origin + [x, 0.0, self.size[2]])
            response.append(origin + [x, 0.0, 0.0])
            response.append(origin + [x, 0.0, 0.0])
            response.append(origin + [x, self.size[1], 0.0])

        return response

    def y_corner(self) -> list:
        # A line of the "Y corner" is (0, y, MAX_Z) -> (0, y, 0) -> (MAX_X, y, 0)
        response = []
        origin = self.origin
        divisions = self.y_divisions

        # Enclose the grid if required
        if self.enclosed:
            divisions = np.append(divisions, self.size[1])

        for y in divisions:
            response.append(origin + [0.0, y, self.size[2]])
            response.append(origin + [0.0, y, 0.0])
            response.append(origin + [0.0, y, 0.0])
            response.append(origin + [self.size[0], y, 0.0])

        return response

    def z_corner(self) -> list:
        # A line of the "Z corner" is (MAX_X, 0, z) -> (0, 0, z) -> (0, MAX_Y, z)
        response = []
        origin = self.origin
        divisions = self.z_divisions

        # Enclose the grid if required
        if self.enclosed:
            divisions = np.append(divisions, self.size[2])

        for z in divisions:
            response.append(origin + [self.size[0], 0.0, z])
            response.append(origin + [0.0, 0.0, z])
            response.append(origin + [0.0, 0.0, z])
            response.append(origin + [0.0, self.size[1], z])

        return response

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1

        # Data
        vertices = self.generate_grid().astype(np.float32)
        self.total_lines = len(vertices)

        # Color
        colors = np.tile(self.grid_color, self.total_lines).astype(np.float32)

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
