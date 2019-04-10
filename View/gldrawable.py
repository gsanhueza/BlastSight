#!/usr/bin/env python

import numpy as np

from OpenGL.GL import *
from PySide2.QtGui import QOpenGLShaderProgram
from PySide2.QtGui import QOpenGLVertexArrayObject
from PySide2.QtGui import QOpenGLBuffer
from PySide2.QtGui import QOpenGLShader


class GLDrawable:
    def __init__(self, opengl_widget):
        self.widget = opengl_widget

        # Shaders
        self.shader_program = QOpenGLShaderProgram(self.widget.context())
        self.vertex_shader = None
        self.fragment_shader = None
        self.geometry_shader = None

        self.vertex_shader_source = None
        self.fragment_shader_source = None
        self.geometry_shader_source = None

        # Vertex {Array/Buffer} Objects
        self.vao = None
        self.positions_vbo = None
        self.values_vbo = None
        self.indices_ibo = None

        # Data
        self.positions = np.array([], np.float32)
        self.indices = np.array([], np.uint32)
        self.values = np.array([], np.float32)

        # FIXME Just for testing
        self.default_data()

    def initialize(self):
        # Remember to set shader sources in children of this class
        # For example:

        # self.set_vertex_shader_source('View/Shaders/mesh_vertex.glsl')
        # self.set_fragment_shader_source('View/Shaders/mesh_fragment.glsl')
        # self.set_geometry_shader_source('View/Shaders/mesh_geometry.glsl')

        # Setup shaders and buffers
        self.initialize_shader_program()
        self.initialize_buffers()

        # Setup vertex attributes
        self.setup_vertex_attribs()

        # Setup uniforms
        self.setup_uniforms()

    def default_data(self):
        self.update_positions(np.array([-0.5, 0.5, 0.0,
                                        -0.5, -0.5, 0.0,
                                        0.5, 0.5, 0.0], np.float32))

        self.update_values(np.array([1.0, 0.0, 0.0,
                                     0.0, 1.0, 0.0,
                                     0.0, 0.0, 1.0], np.float32))

        self.update_indices(np.array([0, 1, 2], np.uint32))  # GL_UNSIGNED_INT = np.uint32

    def set_vertex_shader_source(self, source: str):
        self.vertex_shader_source = source

    def set_fragment_shader_source(self, source: str):
        self.fragment_shader_source = source

    def set_geometry_shader_source(self, source: str):
        self.geometry_shader_source = source

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
        self.vao = QOpenGLVertexArrayObject()
        self.positions_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self.values_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self.indices_ibo = QOpenGLBuffer(QOpenGLBuffer.IndexBuffer)

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

    def setup_uniforms(self):
        pass

    def draw(self):
        pass
