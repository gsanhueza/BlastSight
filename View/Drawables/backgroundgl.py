#!/usr/bin/env python

from OpenGL.GL import *

from PyQt5.QtGui import QOpenGLShaderProgram
from PyQt5.QtGui import QOpenGLVertexArrayObject
from PyQt5.QtGui import QOpenGLShader
from PyQt5.QtGui import QVector4D

from View.Drawables.gldrawable import GLDrawable


class BackgroundGL(GLDrawable):
    def __init__(self, widget, element):
        super().__init__(widget, element)

        # Gradient colors
        self.top_color_loc = None
        self.bot_color_loc = None

    def initialize_program(self) -> None:
        self.shader_program = QOpenGLShaderProgram(self.widget.context())
        self.vao = QOpenGLVertexArrayObject()
        self.vao.create()

    def initialize_shaders(self) -> None:
        vertex_shader = QOpenGLShader(QOpenGLShader.Vertex)
        fragment_shader = QOpenGLShader(QOpenGLShader.Fragment)

        vertex_shader.compileSourceFile('View/Shaders/Background/vertex.glsl')
        fragment_shader.compileSourceFile('View/Shaders/Background/fragment.glsl')

        self.shader_program.addShader(vertex_shader)
        self.shader_program.addShader(fragment_shader)
        self.shader_program.link()

    def setup_uniforms(self) -> None:
        self.top_color_loc = self.shader_program.uniformLocation('top_color')
        self.bot_color_loc = self.shader_program.uniformLocation('bot_color')

    # Taken from http://www.cs.princeton.edu/~mhalber/blog/ogl_gradient/
    def draw(self, proj_matrix=None, view_matrix=None, model_matrix=None):
        self.shader_program.bind()
        self.shader_program.setUniformValue(self.top_color_loc, QVector4D(0.1, 0.1, 0.5, 1.0))
        self.shader_program.setUniformValue(self.bot_color_loc, QVector4D(0.1, 0.1, 0.2, 1.0))

        self.vao.bind()
        glDrawArrays(GL_TRIANGLES, 0, 3)
        self.vao.release()
