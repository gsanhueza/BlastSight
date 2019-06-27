#!/usr/bin/env python

import numpy as np

from qtpy.QtGui import QOpenGLVertexArrayObject
from qtpy.QtGui import QOpenGLBuffer

from .gldrawable import GLDrawable
from OpenGL.GL import *


class TubeGL(GLDrawable):
    def __init__(self, widget=None, element=None):
        super().__init__(widget, element)

        # Sizes
        self.vertices_size = 0
        self.color_size = 0
        self.vao = QOpenGLVertexArrayObject()

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1

        if not self.vao.isCreated():
            self.vao.create()

        # VBO
        vertices_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        color_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)

        vertices_vbo.create()
        color_vbo.create()

        # Data
        vertices = self.element.vertices

        # FIXME If color is the same for each tube, make this an uniform (and we shouldn't need to import numpy)
        color = np.array([self.element.color for _ in range(len(vertices))], np.float32)

        self.vertices_size = vertices.size
        self.color_size = color.size

        self.widget.makeCurrent()
        self.vao.bind()

        vertices_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * self.vertices_size, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None)

        color_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * self.color_size, color, GL_STATIC_DRAW)
        glVertexAttribPointer(_COLOR, 3, GL_FLOAT, False, 0, None)

        glEnableVertexAttribArray(_POSITION)
        glEnableVertexAttribArray(_COLOR)

        self.vao.release()

    def draw(self):
        super().draw()
        if not self.is_visible:
            return

        self.vao.bind()

        # np.array([[0, 1, 2]], type) has size 3, despite having only 1 list there
        glDrawArrays(GL_LINE_STRIP, 0, self.vertices_size)
