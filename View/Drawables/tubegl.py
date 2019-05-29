#!/usr/bin/env python

from PyQt5.QtGui import QOpenGLShaderProgram
from PyQt5.QtGui import QOpenGLVertexArrayObject
from PyQt5.QtGui import QOpenGLBuffer
from PyQt5.QtGui import QOpenGLShader

from View.Drawables.gldrawable import GLDrawable
from OpenGL.GL import *


class TubeGL(GLDrawable):
    def __init__(self, widget=None, element=None):
        super().__init__(widget, element)

        # Uniforms
        self.model_view_matrix_loc = None
        self.proj_matrix_loc = None
        self.block_size_loc = None

        # Sizes
        self.vertices_size = 0
        self.color_size = 0

    def initialize_program(self) -> None:
        self.shader_program = QOpenGLShaderProgram(self.widget.context())
        self.vao = QOpenGLVertexArrayObject()
        self.vao.create()

    def initialize_shaders(self) -> None:
        vertex_shader = QOpenGLShader(QOpenGLShader.Vertex)
        fragment_shader = QOpenGLShader(QOpenGLShader.Fragment)

        vertex_shader.compileSourceFile('View/Shaders/Tube/vertex.glsl')
        fragment_shader.compileSourceFile('View/Shaders/Tube/fragment.glsl')

        self.shader_program.addShader(vertex_shader)
        self.shader_program.addShader(fragment_shader)
        self.shader_program.link()

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1

        # VBO
        vertices_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        color_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)

        vertices_vbo.create()
        color_vbo.create()

        # Data
        import numpy as np

        # TODO Create a polygon with radius (self.element.radius) and resolution (self.element.resolution)
        vertices_ = []
        for v in self.element.vertices:
            vertices_.append([v[0] - 1,
                              v[1] + 0,
                              v[2] + 0])

            vertices_.append([v[0] + 1,
                              v[1] + 0,
                              v[2] + 0])

            vertices_.append([v[0] + 0,
                              v[1] + 1,
                              v[2] + 0])

        vertices = np.array(vertices_, np.float32)

        # FIXME If color is the same for each tube, make this an uniform (and we shouldn't need to import numpy)
        color = np.array([self.element.color for _ in range(len(vertices))], np.float32)

        self.vertices_size = vertices.size
        self.color_size = color.size

        self.widget.makeCurrent()
        self.vao.bind()
        vertices_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * self.vertices_size, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None)

        color_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * self.color_size, color, GL_STATIC_DRAW)
        glVertexAttribPointer(_COLOR, 3, GL_FLOAT, False, 0, None)

        glEnableVertexAttribArray(_POSITION)
        glEnableVertexAttribArray(_COLOR)

        self.vao.release()

    def setup_uniforms(self) -> None:
        self.model_view_matrix_loc = self.shader_program.uniformLocation('model_view_matrix')
        self.proj_matrix_loc = self.shader_program.uniformLocation('proj_matrix')

    def draw(self, proj_matrix, view_matrix, model_matrix) -> None:
        if not self.is_visible:
            return

        self.shader_program.bind()
        self.shader_program.setUniformValue(self.proj_matrix_loc, proj_matrix)
        self.shader_program.setUniformValue(self.model_view_matrix_loc, view_matrix * model_matrix)

        self.vao.bind()

        # np.array([[0, 1, 2]], type) has size 3, despite having only 1 list there
        glDrawArrays(GL_TRIANGLES, 0, self.vertices_size)

        self.vao.release()