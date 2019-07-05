#!/usr/bin/env python

from OpenGL.GL import *

from .gldrawable import GLDrawable


class BackgroundGL(GLDrawable):
    def __init__(self, widget, element):
        super().__init__(widget, element)

    def draw(self):
        glDrawArrays(GL_TRIANGLES, 0, 3)
