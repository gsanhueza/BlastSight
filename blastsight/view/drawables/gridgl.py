#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np

from OpenGL.GL import *
from qtpy.QtGui import QMatrix4x4

from .gldrawable import GLDrawable


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

        # Grid rotation
        self._rotation = np.zeros(3)

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

    @property
    def rotation(self) -> np.array:
        return np.asarray(self._rotation)

    @rotation.setter
    def rotation(self, value: iter) -> None:
        self._rotation = np.asarray(value, np.float32)

    """
    Utilities (Positions are relative to [0.0, 0.0, 0.0])
    """
    @property
    def x_ticks(self) -> np.array:
        flat_divisions = np.ceil(np.arange(0.0, self.x_target[0], self.mark_separation))
        return np.c_[flat_divisions, np.zeros(len(flat_divisions)), np.zeros(len(flat_divisions))]

    @property
    def y_ticks(self) -> np.array:
        flat_divisions = np.ceil(np.arange(0.0, self.y_target[1], self.mark_separation))
        return np.c_[np.zeros(len(flat_divisions)), flat_divisions, np.zeros(len(flat_divisions))]

    @property
    def z_ticks(self) -> np.array:
        flat_divisions = np.ceil(np.arange(0.0, self.z_target[2], self.mark_separation))
        return np.c_[np.zeros(len(flat_divisions)), np.zeros(len(flat_divisions)), flat_divisions]

    @property
    def x_target(self) -> list:
        return [self.size[0], 0.0, 0.0]

    @property
    def y_target(self) -> list:
        return [0.0, self.size[1], 0.0]

    @property
    def z_target(self) -> list:
        return [0.0, 0.0, self.size[2]]

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
        # Detect max difference and expand end
        diff = np.diff([start, end], axis=0)[0]
        diff_sep = diff / separation
        ceil_diff_sep = np.ceil(diff_sep)

        # Generate fake end
        fake_end = separation * ceil_diff_sep

        # Generate linspace
        response = np.linspace(start, fake_end, separation + 1)

        # Truncate last response to fit true end
        response[-1] = end

        return np.asarray(response)

    # Generates a plane using two lines
    def generate_plane(self, line_a: np.array, line_b: np.array) -> list:
        response = list()

        # "Vertical" section
        diff = line_b[-1] - line_a[0]
        for start in line_a:
            response.append(start)
            response.append(start + diff)

        # "Horizontal" section
        diff = line_a[-1] - line_b[0]
        for start in line_b:
            response.append(start)
            response.append(start + diff)

        return response

        # Generates XY/YZ/XZ plane
    def generate_corner(self, start: list, end_x: list, end_y: list, sep_x: int, sep_y: int) -> list:
        line_x = self.generate_line(start, end_x, sep_x)
        line_y = self.generate_line(start, end_y, sep_y)

        return self.generate_plane(line_x, line_y)

    def generate_grid(self) -> np.ndarray:
        marks = []

        # Grid
        marks = np.append(marks, self.xy_flat())
        marks = np.append(marks, self.xz_flat())
        marks = np.append(marks, self.yz_flat())

        # Add true origin to generate the real grid
        marks = self.origin + np.array(marks).reshape((-1, 3)).astype(np.float32)

        # Finally, rotate the marks to fit current grid rotation
        matrix = self.calculate_rotation_matrix()
        rotated_marks = list(map(lambda mark: self.rotate_mark_with_qmatrix(matrix, mark), marks))
        rotated_marks = np.array(rotated_marks)

        return rotated_marks

    def calculate_rotation_matrix(self) -> QMatrix4x4:
        matrix = QMatrix4x4()

        # Translate matrix (translation = rotation_center)
        translation = self.origin
        matrix.translate(*translation)

        # Rotate matrix
        matrix.rotate(self.rotation[0], 1.0, 0.0, 0.0)
        matrix.rotate(self.rotation[1], 0.0, 1.0, 0.0)
        matrix.rotate(self.rotation[2], 0.0, 0.0, 1.0)

        # Restore matrix
        matrix.translate(*-translation)

        return matrix

    @staticmethod
    def rotate_mark_with_qmatrix(matrix: QMatrix4x4, mark: iter) -> np.array:
        # We'd use `QVector4D(*mark, 1.0)`, but PySide2
        # hasn't implemented QMatrix4x4 * QVector4D yet.
        vector = [*mark, 1.0]
        temp_matrix = QMatrix4x4(*[e for e in vector for _ in range(4)])

        response_3d = (matrix * temp_matrix).column(0)
        return np.array([response_3d.x(), response_3d.y(), response_3d.z()])

    def xy_flat(self) -> list:
        return self.generate_corner(
            start=[0.0, 0.0, 0.0],
            end_x=self.x_target,
            end_y=self.y_target,
            sep_x=len(self.x_ticks),
            sep_y=len(self.y_ticks),
        )

    def xz_flat(self) -> list:
        return self.generate_corner(
            start=[0.0, 0.0, 0.0],
            end_x=self.x_target,
            end_y=self.z_target,
            sep_x=len(self.x_ticks),
            sep_y=len(self.z_ticks),
        )

    def yz_flat(self) -> list:
        return self.generate_corner(
            start=[0.0, 0.0, 0.0],
            end_x=self.y_target,
            end_y=self.z_target,
            sep_x=len(self.y_ticks),
            sep_y=len(self.z_ticks),
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
