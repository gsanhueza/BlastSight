#!/usr/bin/env python

import numpy as np

from .gldrawable import GLDrawable
from OpenGL.GL import *


class BlockModelGL(GLDrawable):
    def __init__(self, widget=None, element=None):
        super().__init__(widget, element)

        # Sizes
        self.values_size = 0

        self.min_val = 0.0
        self.max_val = 1.0

        self.vao = None

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1
        _TEMPLATE = 2

        self.vao = glGenVertexArrays(1)

        # VBO
        vertices_vbo = glGenBuffers(1)
        values_vbo = glGenBuffers(1)
        template_vbo = glGenBuffers(1)

        # Data
        template = self.generate_cube(self.element.block_size)
        vertices = self.element.vertices
        values = self.element.values

        self.values_size = values.size
        self.min_val = values.min() if values.size > 0 else 0.0
        self.max_val = values.max() if values.size > 0 else 1.0

        # norm_func = partial(partial(normalize, min_val), max_val)
        # normalized_values = np.vectorize(norm_func, otypes=[np.float32])(values)

        # WARNING colorsys.hsv_to_rgb returns a tuple. but np.vectorize doesn't accept it as tuple
        # hue[0/3, 1/3, 2/3, 3/3] == [red, green, blue, red]
        # values = np.array(list(map(lambda hue: colorsys.hsv_to_rgb(2 * hue / 3, 1.0, 1.0),
        #                            normalized_values)), np.float32)

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, vertices_vbo)
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * vertices.size, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None)

        glBindBuffer(GL_ARRAY_BUFFER, values_vbo)
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * values.size, values, GL_STATIC_DRAW)
        glVertexAttribPointer(_COLOR, 1, GL_FLOAT, False, 0, None)

        glBindBuffer(GL_ARRAY_BUFFER, template_vbo)
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * template.size, template, GL_STATIC_DRAW)
        glVertexAttribPointer(_TEMPLATE, 3, GL_FLOAT, False, 0, None)

        glVertexAttribDivisor(_POSITION, 1)
        glVertexAttribDivisor(_COLOR, 1)
        glVertexAttribDivisor(_TEMPLATE, 0)

        glEnableVertexAttribArray(_POSITION)
        glEnableVertexAttribArray(_COLOR)
        glEnableVertexAttribArray(_TEMPLATE)

        glBindVertexArray(0)

    def draw(self):
        super().draw()
        if not self.is_visible:
            return

        glBindVertexArray(self.vao)
        glDrawArraysInstanced(GL_TRIANGLE_STRIP, 0, 14, self.values_size)

    # Taken from https://stackoverflow.com/questions/28375338/cube-using-single-gl-triangle-strip
    @staticmethod
    def generate_cube(size: np.ndarray) -> np.ndarray:
        size_x = size[0] / 2
        size_y = size[1] / 2
        size_z = size[2] / 2

        cube_strip = [
            -size_x, size_y, size_z,  # Front-top-left
            size_x, size_y, size_z,  # Front-top-right
            -size_x, -size_y, size_z,  # Front-bottom-left
            size_x, -size_y, size_z,  # Front-bottom-right
            size_x, -size_y, -size_z,  # Back-bottom-right
            size_x, size_y, size_z,  # Front-top-right
            size_x, size_y, -size_z,  # Back-top-right
            -size_x, size_y, size_z,  # Front-top-left
            -size_x, size_y, -size_z,  # Back-top-left
            -size_x, -size_y, size_z,  # Front-bottom-left
            -size_x, -size_y, -size_z,  # Back-bottom-left
            size_x, -size_y, -size_z,  # Back-bottom-right
            -size_x, size_y, -size_z,  # Back-top-left
            size_x, size_y, -size_z,  # Back-top-right
        ]

        return np.array(cube_strip, np.float32)
