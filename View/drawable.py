#!/usr/bin/env python

from collections import OrderedDict

from OpenGL.GL import *
from PySide2.QtGui import QOpenGLShaderProgram
from PySide2.QtGui import QOpenGLVertexArrayObject
from PySide2.QtGui import QOpenGLBuffer
from PySide2.QtGui import QOpenGLShader


class Drawable:
    def __init__(self, opengl_widget):
        self.widget = opengl_widget
        # Shaders
        self.shader_program = QOpenGLShaderProgram(self.widget.context())
        self.vertex_shader = None
        self.fragment_shader = None
        self.geometry_shader = None

        self.vertex_shader_source = 'View/Shaders/mesh_vertex.glsl'
        self.fragment_shader_source = 'View/Shaders/mesh_fragment.glsl'
        self.geometry_shader_source = 'View/Shaders/mesh_geometry.glsl'

        # Vertex {Array/Buffer} Objects
        self.vao = QOpenGLVertexArrayObject()
        self.positions_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self.values_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self.indices_ibo = QOpenGLBuffer(QOpenGLBuffer.IndexBuffer)

        self.uniforms = OrderedDict()
        self.attributes = OrderedDict()

        # Data
        self.positions = None
        self.indices = None
        self.values = None

    def initialize_shader_program(self):
        self.vertex_shader = QOpenGLShader(QOpenGLShader.Vertex)
        self.fragment_shader = QOpenGLShader(QOpenGLShader.Fragment)
        self.geometry_shader = QOpenGLShader(QOpenGLShader.Geometry)

        self.vertex_shader.compileSourceFile(self.vertex_shader_source)
        self.fragment_shader.compileSourceFile(self.fragment_shader_source)
        self.geometry_shader.compileSourceFile(self.geometry_shader_source)

        self.shader_program.addShader(self.vertex_shader)
        self.shader_program.addShader(self.fragment_shader)
        self.shader_program.addShader(self.geometry_shader)
        self.shader_program.link()

    def initialize_buffers(self):
        self.vao.create()
        self.positions_vbo.create()
        self.indices_ibo.create()
        self.values_vbo.create()

    def update_positions(self, positions):
        self.positions = positions

    def update_indices(self, indices):
        self.indices = indices

    def update_values(self, values):
        self.values = values

    def setup_vertex_attribs(self):
        _POSITION = 0
        _COLOR = 1

        _SIZE_OF_GL_FLOAT = 4

        self.widget.makeCurrent()
        self.vao.bind()

        self.positions_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, _SIZE_OF_GL_FLOAT * self.positions.size, self.positions, GL_STATIC_DRAW)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None)

        self.values_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, _SIZE_OF_GL_FLOAT * self.values.size, self.values, GL_STATIC_DRAW)
        glVertexAttribPointer(_COLOR, 3, GL_FLOAT, False, 0, None)

        self.indices_ibo.bind()
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(_POSITION)
        glEnableVertexAttribArray(_COLOR)

        self.vao.release()

    def draw(self):
        print("A")
        self.model_view_matrix_loc = self.shader_program.uniformLocation('model_view_matrix')
        self.proj_matrix_loc = self.shader_program.uniformLocation('proj_matrix')
        print("B")

        self.shader_program.bind()
        self.shader_program.setUniformValue(self.proj_matrix_loc, self.widget.proj)
        self.shader_program.setUniformValue(self.model_view_matrix_loc, self.widget.camera * self.widget.world)

        print("C")
        self.vao.bind()
        print("D")

        # glDrawArrays(GL_TRIANGLES, 0, self.mesh_positions.size)  # This works on its own
        # glDrawElements(GL_POINTS, self.mesh_indices.size, GL_UNSIGNED_INT, None)
        glDrawElements(GL_TRIANGLES, self.indices.size, GL_UNSIGNED_INT, None)

        self.vao.release()
