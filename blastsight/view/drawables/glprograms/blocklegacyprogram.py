#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .blockprogram import BlockProgram


class BlockLegacyProgram(BlockProgram):
    def __init__(self, widget):
        super().__init__(widget)
        self.base_name = 'BlockLegacy'

    def setup_shaders(self):
        # Placeholders to avoid early garbage collection
        vs = self.enable_vertex_shader()
        fs = self.enable_fragment_shader()

        self.shader_program.link()
