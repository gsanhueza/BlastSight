#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from OpenGL.GL import glViewport
from .shaderprogram import ShaderProgram


class AxisProgram(ShaderProgram):
    def __init__(self, viewer):
        super().__init__(viewer)
        self.base_name = 'Axis'

    def draw(self) -> None:
        viewport = [self.viewer.devicePixelRatio() * self.viewer.width(),
                    self.viewer.devicePixelRatio() * self.viewer.height()]
        w, h = viewport

        glViewport(w // 100, h // 100, h // 6, h // 6)
        super().draw()
        glViewport(0, 0, viewport[0], viewport[1])
