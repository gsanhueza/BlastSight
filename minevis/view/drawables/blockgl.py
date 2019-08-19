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
        _ALPHA = 3

        if self.vao is None:
            self.vao = glGenVertexArrays(1)
            self.vbos = glGenBuffers(5)

        # Data
        vertices = np.array(self.element.vertices, np.float32)
        block_size = np.array(self.element.block_size, np.float32)
        template, indices = self.generate_cube(block_size)
        colors = self.element.color.astype(np.float32)
        alpha = np.array([self.element.alpha], np.float32)

        self.num_cubes = vertices.size // 3
        self.num_indices = indices.size

        self.widget.makeCurrent()
        glBindVertexArray(self.vao)

        # buffers = [(pointer, basesize, array)...]
        buffers = [(_POSITION, 3, vertices),
                   (_TEMPLATE, 3, template),
                   (_COLOR, 3, colors),
                   (_ALPHA, 1, alpha),
                   ]

        for i, buf in enumerate(buffers):
            pointer, basesize, array = buf
            glBindBuffer(GL_ARRAY_BUFFER, self.vbos[i])
            glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * array.size, array, GL_STATIC_DRAW)
            glVertexAttribPointer(pointer, basesize, GL_FLOAT, False, 0, None)
            glEnableVertexAttribArray(pointer)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vbos[-1])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

        glVertexAttribDivisor(_POSITION, 1)
        glVertexAttribDivisor(_TEMPLATE, 0)
        glVertexAttribDivisor(_COLOR, 1)
        glVertexAttribDivisor(_ALPHA, -1)

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
