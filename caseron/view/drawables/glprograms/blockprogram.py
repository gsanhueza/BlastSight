#!/usr/bin/env python

from .shaderprogram import ShaderProgram


class BlockProgram(ShaderProgram):
    def __init__(self, widget):
        super().__init__(widget)
        self.base_name = 'Block'

    def setup(self) -> None:
        super().setup()
        self.add_uniform_loc('block_size')

    def setup_shaders(self):
        # Placeholders to avoid early garbage collection
        vs = self.enable_vertex_shader()
        fs = self.enable_fragment_shader()
        gs = self.enable_geometry_shader()

        self.shader_program.link()

    def draw(self):
        for drawable in self.drawables:
            self.update_uniform('block_size', *drawable.element.block_size)
            drawable.draw()