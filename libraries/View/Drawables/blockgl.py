#!/usr/bin/env python

import numpy as np

from .gldrawable import GLDrawable
from OpenGL.GL import *


class BlockGL(GLDrawable):
    def __init__(self, widget=None, element=None):
        super().__init__(widget, element)

        self.num_cubes = 0
        self.num_indices = 0

    def setup_attributes(self) -> None:
        _POSITION = 0
        _TEMPLATE = 1
        _COLOR = 2

        if self.vao is None:
            self.vao = glGenVertexArrays(1)
            self.vbos = glGenBuffers(4)

        # Data
        vertices = np.array(self.element.vertices, np.float32)
        values = np.array(self.element.values, np.float32)
        block_size = np.array(self.element.block_size, np.float32)
        template, indices = self.generate_cube(block_size)

        self.num_cubes = values.size
        self.num_indices = indices.size

        self.widget.makeCurrent()
        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbos[0])
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * vertices.size, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbos[1])
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * template.size, template, GL_STATIC_DRAW)
        glVertexAttribPointer(_TEMPLATE, 3, GL_FLOAT, False, 0, None)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbos[2])
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * values.size, values, GL_STATIC_DRAW)
        glVertexAttribPointer(_COLOR, 1, GL_FLOAT, False, 0, None)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vbos[3])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(_POSITION)
        glEnableVertexAttribArray(_TEMPLATE)
        glEnableVertexAttribArray(_COLOR)

        glVertexAttribDivisor(_POSITION, 1)
        glVertexAttribDivisor(_TEMPLATE, 0)
        glVertexAttribDivisor(_COLOR, 1)

        glBindVertexArray(0)

    def draw(self):
        super().draw()
        if not self.is_visible:
            return

        glBindVertexArray(self.vao)
        # np.array([[0, 1, 2]], type) has size 3, despite having only 1 list there
        glDrawElementsInstanced(GL_TRIANGLES, self.num_indices, GL_UNSIGNED_INT, None, self.num_cubes)
        glBindVertexArray(0)

    # Taken from https://stackoverflow.com/questions/28375338/cube-using-single-gl-triangle-strip
    @staticmethod
    def generate_cube(size: np.ndarray) -> tuple:
        cube_vertices = np.array([
            [1, 1, -1],
            [1, -1, -1],
            [1, 1, 1],
            [1, -1, 1],
            [-1, 1, -1],
            [-1, -1, -1],
            [-1, 1, 1],
            [-1, -1, 1],
        ]) * size * 0.5

        cube_indices = np.array([
            [4, 2, 0],
            [2, 7, 3],
            [6, 5, 7],
            [1, 7, 5],
            [0, 3, 1],
            [4, 1, 5],
            [4, 6, 2],
            [2, 6, 7],
            [6, 4, 5],
            [1, 3, 7],
            [0, 2, 3],
            [4, 0, 1],
        ])

        return cube_vertices.astype(np.float32), cube_indices.astype(np.uint32)
