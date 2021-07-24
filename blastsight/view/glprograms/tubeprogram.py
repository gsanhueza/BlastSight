#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .shaderprogram import ShaderProgram
from qtpy.QtGui import QOpenGLShader


class TubeProgram(ShaderProgram):
    def __init__(self):
        super().__init__()
        self.base_name = 'Tube'

    def generate_shaders(self) -> list:
        shaders = super().generate_shaders()
        shaders.append(self.generate_shader(QOpenGLShader.Geometry, self.geometry_path))

        return shaders
