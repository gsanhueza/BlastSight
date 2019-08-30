#!/usr/bin/env python

from OpenGL.GL import *

from .gldrawable import GLDrawable


class BackgroundGL(GLDrawable):
    def __init__(self, widget, element, *args, **kwargs):
        super().__init__(widget, element)

    def draw(self):
        glDisable(GL_DEPTH_TEST)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glEnable(GL_DEPTH_TEST)
