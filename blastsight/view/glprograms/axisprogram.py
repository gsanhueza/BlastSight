#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from OpenGL.GL import glViewport
from .shaderprogram import ShaderProgram


class AxisProgram(ShaderProgram):
    def __init__(self, widget):
        super().__init__(widget)
        self.base_name = 'Axis'

    def draw(self):
        viewport = [self.widget.devicePixelRatio() * self.widget.width(),
                    self.widget.devicePixelRatio() * self.widget.height()]
        w, h = viewport

        glViewport(w // 100, h // 100, h // 6, h // 6)
        super().draw()
        glViewport(0, 0, viewport[0], viewport[1])
