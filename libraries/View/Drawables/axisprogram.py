#!/usr/bin/env python

from qtpy.QtGui import QOpenGLShader
from .shaderprogram import ShaderProgram


class AxisProgram(ShaderProgram):
    def __init__(self, widget):
        super().__init__(widget)

    def setup(self) -> None:
        super().setup()
        self.add_uniform_loc('model_view_matrix')
        self.add_uniform_loc('proj_matrix')

    def setup_shaders(self):
        vertex_shader = QOpenGLShader(QOpenGLShader.Vertex)
        fragment_shader = QOpenGLShader(QOpenGLShader.Fragment)

        vertex_shader.compileSourceFile(f'{self.shader_dir}/Axis/vertex.glsl')
        fragment_shader.compileSourceFile(f'{self.shader_dir}/Axis/fragment.glsl')

        self.shader_program.addShader(vertex_shader)
        self.shader_program.addShader(fragment_shader)
        self.shader_program.link()
