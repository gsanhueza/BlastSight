#!/usr/bin/env python

from PyQt5.QtGui import QOpenGLShaderProgram
from PyQt5.QtGui import QOpenGLVertexArrayObject
from PyQt5.QtGui import QOpenGLShader
from View.Drawables.gldrawable import GLDrawable

from OpenGL.GL import *


class BackgroundGL(GLDrawable):
    def __init__(self, widget, element):
        super().__init__(widget, element)

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

    def setup_attributes(self) -> None:
        pass

    def setup_uniforms(self) -> None:
        pass

    def draw(self, proj_matrix=None, view_matrix=None, model_matrix=None):
        self.shader_program.bind()
        self.vao.bind()
        glDrawArrays(GL_TRIANGLES, 0, 3)
        self.vao.release()
