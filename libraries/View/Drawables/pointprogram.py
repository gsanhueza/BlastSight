#!/usr/bin/env python

import pathlib

from qtpy.QtGui import QVector2D
from qtpy.QtGui import QOpenGLShader
from .shaderprogram import ShaderProgram


class PointProgram(ShaderProgram):
    def __init__(self, widget):
        super().__init__(widget)

    def setup(self) -> None:
        super().setup()
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

    def draw(self):
        for drawable in self.drawables:
            self.update_uniform('point_size', QVector2D(drawable.point_size, 0.0)),
            self.update_uniform('min_max', QVector2D(drawable.min_val, drawable.max_val)),
            drawable.draw()
