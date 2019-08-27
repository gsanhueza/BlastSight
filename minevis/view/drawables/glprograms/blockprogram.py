#!/usr/bin/env python

from OpenGL.GL import *
from qtpy.QtGui import QOpenGLShader
from .shaderprogram import ShaderProgram
from OpenGL.GL import *


class BlockProgram(ShaderProgram):
    def __init__(self, widget):
        super().__init__(widget)

    def setup(self) -> None:
        super().setup()
        self.add_uniform_loc('block_size')

    def setup_shaders(self):
        vertex_shader = QOpenGLShader(QOpenGLShader.Vertex)
        fragment_shader = QOpenGLShader(QOpenGLShader.Fragment)
        geometry_shader = QOpenGLShader(QOpenGLShader.Geometry)

        vertex_shader.compileSourceFile(f'{self.shader_dir}/Block/vertex.glsl')
        fragment_shader.compileSourceFile(f'{self.shader_dir}/Block/fragment.glsl')
        geometry_shader.compileSourceFile(f'{self.shader_dir}/Block/geometry.glsl')

        self.shader_program.addShader(vertex_shader)
        self.shader_program.addShader(fragment_shader)
        self.shader_program.addShader(geometry_shader)
        self.shader_program.link()

    def draw(self):
        glEnable(GL_CULL_FACE)
        for drawable in self.drawables:
            self.update_uniform('block_size', *drawable.element.block_size)
            drawable.draw()
        glDisable(GL_CULL_FACE)
