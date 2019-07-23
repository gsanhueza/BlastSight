#!/usr/bin/env python

import pathlib

from qtpy.QtGui import QOpenGLShader
from qtpy.QtGui import QOpenGLShaderProgram


class ShaderProgram:
    def __init__(self, widget):
        self.widget = widget
        self.shader_program = None
        self.shader_dir = f'{pathlib.Path(__file__).parent.parent}/Shaders'
        self.uniform_locs = {}

    def setup(self) -> None:
        if self.shader_program:
            return

        self.shader_program = QOpenGLShaderProgram(self.widget.context())
        self.setup_shaders()

        self.add_uniform_loc('model_view_matrix')
        self.add_uniform_loc('proj_matrix')

    def setup_shaders(self) -> None:
        # Shaders
        vertex_shader = QOpenGLShader(QOpenGLShader.Vertex)
        fragment_shader = QOpenGLShader(QOpenGLShader.Fragment)

        vertex_shader.compileSourceFile(f'{self.shader_dir}/Background/vertex.glsl')
        fragment_shader.compileSourceFile(f'{self.shader_dir}/Background/fragment.glsl')

        self.shader_program.addShader(vertex_shader)
        self.shader_program.addShader(fragment_shader)
        self.shader_program.link()

    def add_uniform_loc(self, loc_str) -> None:
        self.uniform_locs[loc_str] = self.shader_program.uniformLocation(loc_str)

    def update_uniform(self, loc_str, *values) -> None:
        self.shader_program.setUniformValue(self.uniform_locs[loc_str], *values)

    def set_drawables(self, drawables):
        self.drawables = drawables

    def draw(self):
        for drawable in self.drawables:
            drawable.draw()

    def bind(self) -> None:
        self.shader_program.bind()
