#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from colour import Color
from OpenGL.GL import *

from .gldrawable import GLDrawable


class BackgroundGL(GLDrawable):
    def __init__(self, element=None, *args, **kwargs):
        super().__init__(element, *args, **kwargs)
        self._top_color = [0.1, 0.2, 0.3, 1.0]
        self._bottom_color = [0.4, 0.5, 0.6, 1.0]

    @property
    def top_color(self) -> list:
        return self._top_color

    @property
    def bottom_color(self) -> list:
        return self._bottom_color

    @top_color.setter
    def top_color(self, color: list) -> None:
        self._top_color = color
        self.notify()

    @bottom_color.setter
    def bottom_color(self, color: list) -> None:
        self._bottom_color = color
        self.notify()

    def draw(self) -> None:
        glDisable(GL_DEPTH_TEST)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glEnable(GL_DEPTH_TEST)
