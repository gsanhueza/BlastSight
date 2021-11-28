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

    def generate_line(self, start: iter, end: iter, separation: int) -> np.ndarray:
        return np.linspace(start, end, separation + 1)

    def generate_flat(self, line_a: np.array, line_b: np.array) -> list:
        response = list()

        # "Vertical" section
        diff = line_b[-1] - line_a[0]
        for start in line_a:
            response.append(start)
            response.append(start + diff)

        # "Horizontal section"
        diff = line_a[-1] - line_b[0]
        for start in line_b:
            response.append(start)
            response.append(start + diff)

        return response

    def generate_corner(self, start: list, end_x: list, end_y: list, sep_x: int, sep_y: int) -> list:
        line_x = self.origin + self.generate_line(start, end_x, sep_x)
        line_y = self.origin + self.generate_line(start, end_y, sep_y)

        return self.generate_flat(line_x, line_y)

    def generate_grid(self) -> np.ndarray:
        marks = []

        # Grid
        marks += self.xy_flat()
        marks += self.xz_flat()
        marks += self.yz_flat()

        return np.array(marks).reshape((-1, 3)).astype(np.float32)

    def xy_flat(self) -> list:
        return self.generate_corner(
            start=[0.0, 0.0, 0.0],
            end_x=[self.size[0], 0.0, 0.0],
            end_y=[0.0, self.size[1], 0.0],
            sep_x=len(self.x_divisions),
            sep_y=len(self.y_divisions)
        )

    def xz_flat(self) -> list:
        return self.generate_corner(
            start=[0.0, 0.0, 0.0],
            end_x=[self.size[0], 0.0, 0.0],
            end_y=[0.0, 0.0, self.size[2]],
            sep_x=len(self.x_divisions),
            sep_y=len(self.z_divisions)
        )

    def yz_flat(self) -> list:
        return self.generate_corner(
            start=[0.0, 0.0, 0.0],
            end_x=[0.0, self.size[1], 0.0],
            end_y=[0.0, 0.0, self.size[2]],
            sep_x=len(self.y_divisions),
            sep_y=len(self.z_divisions)
        )

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
