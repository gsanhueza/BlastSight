#!/usr/bin/env python

from qtpy.QtGui import QOpenGLShaderProgram
from qtpy.QtGui import QOpenGLVertexArrayObject
from qtpy.QtGui import QVector2D
from qtpy.QtGui import QOpenGLBuffer
from qtpy.QtGui import QOpenGLShader

from .gldrawable import GLDrawable
from OpenGL.GL import *


class PointGL(GLDrawable):
    def __init__(self, widget=None, element=None):
        super().__init__(widget, element)

        # Uniforms
        self.point_size_loc = None

        # Sizes
        self.vertices_size = 0
        self.values_size = 0

        self.min_val = 0.0
        self.max_val = 1.0

    def initialize_program(self) -> None:
        self.shader_program = QOpenGLShaderProgram(self.widget.context())
        self.vao = QOpenGLVertexArrayObject()
        self.vao.create()

    def initialize_shaders(self) -> None:
        vertex_shader = QOpenGLShader(QOpenGLShader.Vertex)
        fragment_shader = QOpenGLShader(QOpenGLShader.Fragment)
        vertex_shader.compileSourceFile(f'{self._shader_dir}/Point/vertex.glsl')
        fragment_shader.compileSourceFile(f'{self._shader_dir}/Point/fragment.glsl')

        self.shader_program.addShader(vertex_shader)
        self.shader_program.addShader(fragment_shader)
        self.shader_program.link()

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1

        # VBO
        vertices_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        values_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)

        vertices_vbo.create()
        values_vbo.create()

        # Data
        vertices = self.element.vertices
        values = self.element.values

        self.min_val = values.min() if values.size > 0 else 0.0
        self.max_val = values.max() if values.size > 0 else 1.0

        self.vertices_size = vertices.size
        self.values_size = values.size

        self.widget.makeCurrent()
        self.vao.bind()

        vertices_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * self.vertices_size, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None)

        values_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * self.values_size, values, GL_STATIC_DRAW)
        glVertexAttribPointer(_COLOR, 1, GL_FLOAT, False, 0, None)

        glEnableVertexAttribArray(_POSITION)
        glEnableVertexAttribArray(_COLOR)

        self.vao.release()

    def setup_uniforms(self) -> None:
        self.model_view_matrix_loc = self.shader_program.uniformLocation('model_view_matrix')
        self.proj_matrix_loc = self.shader_program.uniformLocation('proj_matrix')

        self.point_size_loc = self.shader_program.uniformLocation('point_size')
        self.min_max_loc = self.shader_program.uniformLocation('min_max')

        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)

    def draw(self, proj_matrix=None, view_matrix=None, model_matrix=None):
        if not self.is_visible:
            return

        self.shader_program.bind()
        self.shader_program.setUniformValue(self.proj_matrix_loc, proj_matrix)
        self.shader_program.setUniformValue(self.model_view_matrix_loc, view_matrix * model_matrix)
        self.shader_program.setUniformValue(self.point_size_loc, QVector2D(self.element.point_size, 0.0))
        self.shader_program.setUniformValue(self.min_max_loc, QVector2D(self.min_val, self.max_val))

        self.vao.bind()

        # np.array([[0, 1, 2]], type) has size 3, despite having only 1 list there
        glDrawArrays(GL_POINTS, 0, self.vertices_size // 3)

        self.vao.release()
