#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .shaderprogram import ShaderProgram


class XSectionBlockProgram(ShaderProgram):
    def __init__(self):
        super().__init__()
        self.base_name = 'XSectionBlock'

    def initialize(self) -> None:
        super().initialize()
        self.add_uniform_handler('viewport')
        self.add_uniform_handler('block_size')
        self.add_uniform_handler('plane_origin')
        self.add_uniform_handler('plane_normal')

    def setup_shaders(self) -> None:
        # Placeholders to avoid early garbage collection
        vs = self.enable_vertex_shader()
        fs = self.enable_fragment_shader()
        gs = self.enable_geometry_shader()

        self.shader_program.link()

    def inner_draw(self, drawables: list) -> None:
        for drawable in drawables:
            self.update_uniform('block_size', *drawable.element.block_size)
            drawable.draw()

