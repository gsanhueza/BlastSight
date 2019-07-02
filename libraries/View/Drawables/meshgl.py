#!/usr/bin/env python

from qtpy.QtGui import QOpenGLBuffer
from qtpy.QtGui import QOpenGLVertexArrayObject
from .gldrawable import GLDrawable
from OpenGL.GL import *


class MeshGL(GLDrawable):
    def __init__(self, widget=None, element=None):
        super().__init__(widget, element)

        # Uniforms
        self.color = self.element.values
        self.alpha = self.element.alpha

        # Sizes
        self.vertices_size = 0
        self.indices_size = 0

        # Wireframe
        self.wireframe_enabled = False
        self.vao = QOpenGLVertexArrayObject()

    def toggle_wireframe(self) -> bool:
        self.wireframe_enabled = not self.wireframe_enabled
        return self.wireframe_enabled

    def disable_wireframe(self) -> None:
        self.wireframe_enabled = False

    def enable_wireframe(self):
        self.wireframe_enabled = True

    def setup_attributes(self) -> None:
        _POSITION = 0

        if not self.vao.isCreated():
            self.vao.create()

        # VBO
        vertices_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        indices_ibo = QOpenGLBuffer(QOpenGLBuffer.IndexBuffer)
        values_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)

        vertices_vbo.create()
        indices_ibo.create()
        values_vbo.create()

        # Data
        vertices = self.element.vertices
        indices = self.element.indices

        self.vertices_size = vertices.size
        self.indices_size = indices.size

        self.widget.makeCurrent()
        self.vao.bind()

        vertices_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * self.vertices_size, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None)

        indices_ibo.bind()
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(_POSITION)

        self.vao.release()

    def draw(self):
        super().draw()
        if not self.is_visible:
            return

        self.vao.bind()
        glDrawElements(GL_TRIANGLES, self.indices_size, GL_UNSIGNED_INT, None)