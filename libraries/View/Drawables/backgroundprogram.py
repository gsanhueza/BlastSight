#!/usr/bin/env python

import pathlib

from qtpy.QtGui import QOpenGLShader
from .shaderprogram import ShaderProgram


class BackgroundProgram(ShaderProgram):
    def __init__(self, widget):
        super().__init__(widget)

    def setup(self) -> None:
        super().setup()
        self.add_uniform_loc('top_color')
        self.add_uniform_loc('bot_color')

    def setup_shaders(self) -> None:
        # Shaders
        shader_dir = f'{pathlib.Path(__file__).parent}/../Shaders'
        vertex_shader = QOpenGLShader(QOpenGLShader.Vertex)
        fragment_shader = QOpenGLShader(QOpenGLShader.Fragment)

        vertex_shader.compileSourceFile(f'{shader_dir}/Background/vertex.glsl')
        fragment_shader.compileSourceFile(f'{shader_dir}/Background/fragment.glsl')

        self.shader_program.addShader(vertex_shader)
        self.shader_program.addShader(fragment_shader)
        self.shader_program.link()
