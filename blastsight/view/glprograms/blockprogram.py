#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .shaderprogram import ShaderProgram
from qtpy.QtGui import QOpenGLShader


class BlockProgram(ShaderProgram):
    def __init__(self):
        super().__init__()
        self.base_name = 'Block'

    def initialize(self) -> None:
        super().initialize()
        self.add_uniform_handler('block_size')

    def generate_shaders(self) -> list:
        shaders = super().generate_shaders()
        shaders.append(self.generate_shader(QOpenGLShader.Geometry, self.geometry_path))

        return shaders

    def inner_draw(self, drawables: list) -> None:
        for drawable in drawables:
            self.update_uniform('block_size', *drawable.element.block_size)
            drawable.draw()
