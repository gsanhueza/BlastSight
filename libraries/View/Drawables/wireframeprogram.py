#!/usr/bin/env python

import pathlib

from qtpy.QtGui import QOpenGLShader
from qtpy.QtGui import QOpenGLShaderProgram


class WireframeProgram:
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.shader_program = None

        self.uniform_locs = {}

    def setup_program(self) -> None:
        if self.shader_program:
            return

        self.shader_program = QOpenGLShaderProgram(self.widget.context())
        self.setup_shaders()

        self.add_uniform_loc('model_view_matrix')
        self.add_uniform_loc('proj_matrix')
        self.add_uniform_loc('u_color')

    def setup_shaders(self):
        # Shaders
        shader_dir = f'{pathlib.Path(__file__).parent}/../Shaders'
        vertex_shader = QOpenGLShader(QOpenGLShader.Vertex)
        fragment_shader = QOpenGLShader(QOpenGLShader.Fragment)
        geometry_shader = QOpenGLShader(QOpenGLShader.Geometry)

        vertex_shader.compileSourceFile(f'{shader_dir}/Mesh/vertex.glsl')
        fragment_shader.compileSourceFile(f'{shader_dir}/Mesh/fragment_wireframe.glsl')
        geometry_shader.compileSourceFile(f'{shader_dir}/Mesh/geometry.glsl')

        self.shader_program.addShader(vertex_shader)
        self.shader_program.addShader(fragment_shader)
        self.shader_program.addShader(geometry_shader)
        self.shader_program.link()

    def add_uniform_loc(self, loc_str):
        self.uniform_locs[loc_str] = self.shader_program.uniformLocation(loc_str)

    def update_uniform(self, loc_str, *values):
        self.shader_program.setUniformValue(self.uniform_locs[loc_str], *values)

    def bind(self):
        self.shader_program.bind()
