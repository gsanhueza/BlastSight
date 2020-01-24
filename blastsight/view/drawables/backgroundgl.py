#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from OpenGL.GL import *

from .gldrawable import GLDrawable


class BackgroundGL(GLDrawable):
    def __init__(self, element=None, *args, **kwargs):
        super().__init__(element, *args, **kwargs)
        self._top_color = [0.1, 0.2, 0.3]
        self._bot_color = [0.4, 0.5, 0.6]

    @property
    def top_color(self) -> list:
        return self._top_color

    @property
    def bot_color(self) -> list:
        return self._bot_color

    @top_color.setter
    def top_color(self, color: list) -> None:
        self._top_color = color
        self.notify()

    @bot_color.setter
    def bot_color(self, color: list) -> None:
        self._bot_color = color
        self.notify()

    def __dir__(self) -> list:
        return sorted(set(dir(type(self)) + list(self.__dict__.keys())))

    def draw(self) -> None:
        glDisable(GL_DEPTH_TEST)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glEnable(GL_DEPTH_TEST)
