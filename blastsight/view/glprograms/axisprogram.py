#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from OpenGL.GL import glViewport
from .shaderprogram import ShaderProgram


class AxisProgram(ShaderProgram):
    def __init__(self):
        super().__init__()
        self.base_name = 'Axis'

    def initialize(self) -> None:
        super().initialize()
        self.add_uniform_handler('viewport')

    def draw(self) -> None:
        w, h = map(int, self.uniform_values.get('viewport'))
        glViewport(w // 100, h // 100, h // 6, h // 6)
        super().draw()
        glViewport(0, 0, w, h)
