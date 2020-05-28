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

        # FIXME The user has to set these values, not us!
        self.plane_origin = [0.0, 0.0, 0.0]
        self.plane_normal = [0.0, 0.0, 1.0]

    def initialize(self) -> None:
        super().initialize()
        self.add_uniform_loc('plane_origin')
        self.add_uniform_loc('plane_normal')

    def setup_shaders(self) -> None:
        # Placeholders to avoid early garbage collection
        vs = self.enable_vertex_shader()
        fs = self.enable_fragment_shader()
        gs = self.enable_geometry_shader()

        self.shader_program.link()

    def inner_draw(self, drawables: list) -> None:
        self.update_uniform('plane_origin', *self.plane_origin)
        self.update_uniform('plane_normal', *self.plane_normal)

        for drawable in drawables:
            drawable.draw()
