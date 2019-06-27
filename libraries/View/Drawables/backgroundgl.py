#!/usr/bin/env python

from OpenGL.GL import *

from qtpy.QtGui import QOpenGLVertexArrayObject
from .gldrawable import GLDrawable


class BackgroundGL(GLDrawable):
    def __init__(self, widget, element):
        super().__init__(widget, element)
        self.vao = QOpenGLVertexArrayObject()

    # Taken from http://www.cs.princeton.edu/~mhalber/blog/ogl_gradient/
    def draw(self):
        super().draw()
        if not self.vao.isCreated():
            self.vao.create()

        self.vao.bind()
        glDrawArrays(GL_TRIANGLES, 0, 3)
