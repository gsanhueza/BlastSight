#!/usr/bin/env python

from qtpy.QtGui import QOpenGLShader
from .meshprogram import MeshProgram


class WireframeProgram(MeshProgram):
    def __init__(self, widget):
        super().__init__(widget)

    def setup_shaders(self):
        vertex_shader = QOpenGLShader(QOpenGLShader.Vertex)
        fragment_shader = QOpenGLShader(QOpenGLShader.Fragment)
        geometry_shader = QOpenGLShader(QOpenGLShader.Geometry)

        vertex_shader.compileSourceFile(f'{self.shader_dir}/Mesh/vertex.glsl')
        fragment_shader.compileSourceFile(f'{self.shader_dir}/Mesh/fragment_wireframe.glsl')
        geometry_shader.compileSourceFile(f'{self.shader_dir}/Mesh/geometry.glsl')

        self.shader_program.addShader(vertex_shader)
        self.shader_program.addShader(fragment_shader)
        self.shader_program.addShader(geometry_shader)
        self.shader_program.link()
