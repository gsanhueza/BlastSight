#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import pathlib

from qtpy.QtGui import QOpenGLContext
from qtpy.QtGui import QOpenGLShader
from qtpy.QtGui import QOpenGLShaderProgram


class ShaderProgram:
    def __init__(self):
        self.base_name = None
        self.shader_program = None
        self.shader_dir = f'{pathlib.Path(__file__).parent}/shaders'

        self.uniform_locations = {}
        self.uniform_values = {}

        self.opaques = []
        self.transparents = []

    @property
    def drawables(self) -> list:
        return self.opaques + self.transparents

    def get_base_name(self) -> str:
        return self.base_name

    def initialize(self) -> None:
        self.shader_program = QOpenGLShaderProgram(QOpenGLContext.currentContext())
        self.setup_shaders()

        self.add_uniform_handler('model_view_matrix')
        self.add_uniform_handler('proj_matrix')

    def setup_shaders(self) -> None:
        # Placeholders to avoid early garbage collection
        vs = self.enable_vertex_shader()
        fs = self.enable_fragment_shader()

        self.shader_program.link()

    def _enable_shader(self, shader_type, filename: str) -> QOpenGLShader:
        shader = QOpenGLShader(shader_type)
        shader.compileSourceFile(f'{self.shader_dir}/{self.base_name}/{filename}')
        self.shader_program.addShader(shader)
        return shader

    def enable_vertex_shader(self, filename='vertex.glsl') -> QOpenGLShader:
        return self._enable_shader(QOpenGLShader.Vertex, filename)

    def enable_fragment_shader(self, filename='fragment.glsl') -> QOpenGLShader:
        return self._enable_shader(QOpenGLShader.Fragment, filename)

    def enable_geometry_shader(self, filename='geometry.glsl') -> QOpenGLShader:
        return self._enable_shader(QOpenGLShader.Geometry, filename)

    def add_uniform_handler(self, loc_str) -> None:
        self.uniform_locations[loc_str] = self.shader_program.uniformLocation(loc_str)

    def update_uniform(self, loc_str, *values) -> None:
        if loc_str in self.uniform_locations.keys():
            self.uniform_values[loc_str] = values
            self.shader_program.bind()
            self.shader_program.setUniformValue(self.uniform_locations[loc_str], *values)

    def set_drawables(self, drawables: list) -> None:
        self.opaques = [d for d in drawables if d.alpha >= 0.99]
        self.transparents = [d for d in drawables if d.alpha < 0.99]

        for drawable in self.drawables:
            drawable.initialize()

    def bind(self) -> None:
        self.shader_program.bind()

    def inner_draw(self, drawables: list) -> None:
        for drawable in drawables:
            drawable.draw()

    def draw(self) -> None:
        self.inner_draw(self.opaques)

    def redraw(self) -> None:
        self.inner_draw(self.transparents)
