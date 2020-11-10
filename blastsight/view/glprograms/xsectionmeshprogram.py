#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from OpenGL.GL import *
from .shaderprogram import ShaderProgram


class XSectionMeshProgram(ShaderProgram):
    def __init__(self):
        super().__init__()
        self.base_name = 'XSectionMesh'

    def initialize(self) -> None:
        super().initialize()
        self.add_uniform_handler('plane_origin')
        self.add_uniform_handler('plane_normal')

    def setup_shaders(self) -> None:
        # Placeholders to avoid early garbage collection
        vs = self.enable_vertex_shader()
        fs = self.enable_fragment_shader()
        gs = self.enable_geometry_shader()

        self.shader_program.link()

    def inner_draw(self, drawables: list) -> None:
        glDisable(GL_DEPTH_TEST)
        glLineWidth(10)
        super().inner_draw(drawables)
        glLineWidth(1)
        glEnable(GL_DEPTH_TEST)
