#!/usr/bin/env python

from qtpy.QtGui import QOpenGLShaderProgram
from qtpy.QtGui import QOpenGLVertexArrayObject
from qtpy.QtGui import QVector2D
from qtpy.QtGui import QOpenGLBuffer
from qtpy.QtGui import QOpenGLShader

from .gldrawable import GLDrawable
from OpenGL.GL import *


class PointGL(GLDrawable):
    def __init__(self, widget=None, element=None):
        super().__init__(widget, element)

        # Sizes
        self.vertices_size = 0
        self.values_size = 0

        self.min_val = 0.0
        self.max_val = 1.0

        self.point_size = element.point_size
        self.vao = QOpenGLVertexArrayObject()

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1

        if not self.vao.isCreated():
            self.vao.create()

        # VBO
        vertices_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        values_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)

        vertices_vbo.create()
        values_vbo.create()

        # Data
        vertices = self.element.vertices
        values = self.element.values

        self.min_val = values.min() if values.size > 0 else 0.0
        self.max_val = values.max() if values.size > 0 else 1.0

        self.vertices_size = vertices.size
        self.values_size = values.size

        self.widget.makeCurrent()
        self.vao.bind()

        vertices_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * self.vertices_size, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None)

        values_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * self.values_size, values, GL_STATIC_DRAW)
        glVertexAttribPointer(_COLOR, 1, GL_FLOAT, False, 0, None)

        glEnableVertexAttribArray(_POSITION)
        glEnableVertexAttribArray(_COLOR)

        self.vao.release()

    def draw(self):
        super().draw()
        if not self.is_visible:
            return

        self.vao.bind()
        # np.array([[0, 1, 2]], type) has size 3, despite having only 1 list there
        glDrawArrays(GL_POINTS, 0, self.vertices_size // 3)
