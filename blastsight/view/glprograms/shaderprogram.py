#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import pathlib

from qtpy.QtGui import QOpenGLShader
from qtpy.QtGui import QOpenGLShaderProgram


class ShaderProgram:
    def __init__(self):
        self.base_name = None
        self.base_folder = f'{pathlib.Path(__file__).parent}/shaders'
        self.shader_program = None

        self.uniform_locations = {}
        self.uniform_values = {}

        self.opaques = []
        self.transparents = []

    @property
    def vertex_path(self) -> str:
        return f'{self.base_folder}/{self.base_name}/vertex.glsl'

    @property
    def fragment_path(self) -> str:
        return f'{self.base_folder}/{self.base_name}/fragment.glsl'

    @property
    def geometry_path(self) -> str:
        return f'{self.base_folder}/{self.base_name}/geometry.glsl'

    @property
    def drawables(self) -> list:
        return self.opaques + self.transparents

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    def initialize(self) -> None:
        self.shader_program = QOpenGLShaderProgram()
        self.generate_shaders()
        self.link_shaders()

        self.add_uniform_handler('model_view_matrix')
        self.add_uniform_handler('proj_matrix')
        self.add_uniform_handler('rendering_offset')

    def generate_shader(self, shader_type, shader_path: str) -> QOpenGLShader:
        shader = QOpenGLShader(shader_type)
        shader.compileSourceFile(shader_path)
        self.shader_program.addShader(shader)

        return shader

    def generate_shaders(self) -> list:
        shaders = list()
        shaders.append(self.generate_shader(QOpenGLShader.Vertex, self.vertex_path))
        shaders.append(self.generate_shader(QOpenGLShader.Fragment, self.fragment_path))

        return shaders

    def link_shaders(self) -> None:
        self.shader_program.link()

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
