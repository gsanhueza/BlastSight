#!/usr/bin/env python

from qtpy.QtGui import QOpenGLShader
from .shaderprogram import ShaderProgram


class BackgroundProgram(ShaderProgram):
    def __init__(self, widget):
        super().__init__(widget)
        self.color_set = False

    def setup(self) -> None:
        super().setup()
        self.add_uniform_loc('top_color')
        self.add_uniform_loc('bot_color')

    def setup_shaders(self) -> None:
        vertex_shader = QOpenGLShader(QOpenGLShader.Vertex)
        fragment_shader = QOpenGLShader(QOpenGLShader.Fragment)

        vertex_shader.compileSourceFile(f'{self.shader_dir}/Background/vertex.glsl')
        fragment_shader.compileSourceFile(f'{self.shader_dir}/Background/fragment.glsl')

        self.shader_program.addShader(vertex_shader)
        self.shader_program.addShader(fragment_shader)
        self.shader_program.link()

    def draw(self):
        if not self.color_set:
            self.update_uniform('top_color', 0.1, 0.2, 0.3, 1.0)
            self.update_uniform('bot_color', 0.4, 0.5, 0.6, 1.0)
        super().draw()
