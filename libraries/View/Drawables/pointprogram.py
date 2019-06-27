#!/usr/bin/env python

import pathlib

from qtpy.QtGui import QOpenGLShader
from .shaderprogram import ShaderProgram


class PointProgram(ShaderProgram):
    def __init__(self, widget):
        super().__init__(widget)

    def setup_program(self) -> None:
        super().setup_program()
        self.add_uniform_loc('model_view_matrix')
        self.add_uniform_loc('proj_matrix')
        self.add_uniform_loc('point_size')
        self.add_uniform_loc('min_max')

    def setup_shaders(self):
        # Shaders
        shader_dir = f'{pathlib.Path(__file__).parent}/../Shaders'
        vertex_shader = QOpenGLShader(QOpenGLShader.Vertex)
        fragment_shader = QOpenGLShader(QOpenGLShader.Fragment)

        vertex_shader.compileSourceFile(f'{shader_dir}/Point/vertex.glsl')
        fragment_shader.compileSourceFile(f'{shader_dir}/Point/fragment.glsl')

        self.shader_program.addShader(vertex_shader)
        self.shader_program.addShader(fragment_shader)
        self.shader_program.link()
