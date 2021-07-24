#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from OpenGL.GL import *
from qtpy.QtGui import QOpenGLShader

from .shaderprogram import ShaderProgram


class XSectionMeshProgram(ShaderProgram):
    def __init__(self):
        super().__init__()
        self.base_name = 'XSectionMesh'

    def initialize(self) -> None:
        super().initialize()
        self.add_uniform_handler('plane_origin')
        self.add_uniform_handler('plane_normal')

    def generate_shaders(self) -> list:
        shaders = super().generate_shaders()
        shaders.append(self.generate_shader(QOpenGLShader.Geometry, self.geometry_path))

        return shaders

    def inner_draw(self, drawables: list) -> None:
        glDisable(GL_DEPTH_TEST)

        # Each mesh can have its own cross-section line width
        for drawable in drawables:
            glLineWidth(drawable.cross_section_width)
            drawable.draw()

        glLineWidth(1)
        glEnable(GL_DEPTH_TEST)
