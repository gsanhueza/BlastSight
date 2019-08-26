#!/usr/bin/env python

from qtpy.QtGui import QOpenGLShader
from .meshprogram import MeshProgram
from OpenGL.GL import *


class WireframeProgram(MeshProgram):
    def __init__(self, widget):
        super().__init__(widget)

    def setup_shaders(self):
        vertex_shader = QOpenGLShader(QOpenGLShader.Vertex)
        fragment_shader = QOpenGLShader(QOpenGLShader.Fragment)

        vertex_shader.compileSourceFile(f'{self.shader_dir}/Mesh/vertex.glsl')
        fragment_shader.compileSourceFile(f'{self.shader_dir}/Mesh/fragment_wireframe.glsl')

        self.shader_program.addShader(vertex_shader)
        self.shader_program.addShader(fragment_shader)
        self.shader_program.link()

    def draw(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        for drawable in self.drawables:
            drawable.draw()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
