#!/usr/bin/env python

from OpenGL.GL import *

from .gldrawable import GLDrawable


class BackgroundGL(GLDrawable):
    def __init__(self, element, *args, **kwargs):
        super().__init__(element)

    def __dir__(self):
        return sorted(set(dir(type(self)) + list(self.__dict__.keys())))

    def draw(self):
        if not self.is_visible:
            return

        glDisable(GL_DEPTH_TEST)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glEnable(GL_DEPTH_TEST)
