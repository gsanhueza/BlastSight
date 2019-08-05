#!/usr/bin/env python

import numpy as np

from .gldrawable import GLDrawable
from OpenGL.GL import *


class TubeGL(GLDrawable):
    def __init__(self, widget=None, element=None):
        super().__init__(widget, element)

        self.vertices_size = 0
        self.vao = None

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1
        _PROPERTIES = 2  # [radius, resolution]

        self.vao = glGenVertexArrays(1)
        self.vbos = glGenBuffers(3)

        # Data
        vertices = self.element.vertices

        # np.array([[0, 1, 2]], type) has size 3, despite having only 1 list there
        self.vertices_size = vertices.size // 3

        colors = np.array(np.tile(self.element.rgba, self.vertices_size), np.float32)
        properties = np.array(np.tile(
            np.append(self.element.radius, self.element.resolution), self.vertices_size), np.float32)

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbos[0])
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * vertices.size, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbos[1])
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * colors.size, colors, GL_STATIC_DRAW)
        glVertexAttribPointer(_COLOR, 4, GL_FLOAT, False, 0, None)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbos[2])
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * properties.size, properties, GL_STATIC_DRAW)
        glVertexAttribPointer(_PROPERTIES, 2, GL_FLOAT, False, 0, None)

        glEnableVertexAttribArray(_POSITION)
        glEnableVertexAttribArray(_COLOR)
        glEnableVertexAttribArray(_PROPERTIES)

        glBindVertexArray(0)

    def draw(self):
        super().draw()
        if not self.is_visible:
            return

        glBindVertexArray(self.vao)
        glDrawArrays(GL_LINE_STRIP, 0, self.vertices_size)
        glBindVertexArray(0)
