#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .shaderprogram import ShaderProgram


class CrossSectionProgram(ShaderProgram):
    def __init__(self, viewer):
        super().__init__(viewer)
        self.base_name = 'CrossSection'

    def initialize(self) -> None:
        super().initialize()
        self.add_uniform_loc('plane_origin')
        self.add_uniform_loc('plane_normal')

        # Default values
        self.update_uniform('plane_origin', *[0.0, 0.0, 0.0])
        self.update_uniform('plane_normal', *[1.0, 0.0, 0.0])

    def setup_shaders(self) -> None:
        # Placeholders to avoid early garbage collection
        vs = self.enable_vertex_shader()
        fs = self.enable_fragment_shader()
        gs = self.enable_geometry_shader()

        self.shader_program.link()
