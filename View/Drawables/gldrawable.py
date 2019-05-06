#!/usr/bin/env python

from OpenGL.GL import *
from PyQt5.QtGui import QOpenGLShaderProgram
from PyQt5.QtGui import QOpenGLVertexArrayObject
from PyQt5.QtGui import QOpenGLBuffer
from PyQt5.QtGui import QOpenGLShader


class GLDrawable:
    def __init__(self, opengl_widget, model_element):
        super().__init__()
        self.widget = opengl_widget
        self.model_element = model_element

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

        self.is_initialized = False
        self.is_visible = True

        # Sizes
        self.vertices_size = 0
        self.indices_size = 0
        self.values_size = 0

    def show(self) -> None:
        self.is_visible = True

    def hide(self) -> None:
        self.is_visible = False

    def get_model_element(self):
        return self.model_element

    def initialize(self) -> None:
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

        self.is_initialized = True

    def set_vertex_shader_source(self, source: str) -> None:
        self.vertex_shader_source = source

    def set_fragment_shader_source(self, source: str) -> None:
        self.fragment_shader_source = source

    def set_geometry_shader_source(self, source: str) -> None:
        self.geometry_shader_source = source

    def initialize_shader_program(self) -> None:
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

    def initialize_buffers(self) -> None:
        self.vao = QOpenGLVertexArrayObject()
        self.positions_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self.values_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self.indices_ibo = QOpenGLBuffer(QOpenGLBuffer.IndexBuffer)

        self.vao.create()
        self.positions_vbo.create()
        self.indices_ibo.create()
        self.values_vbo.create()

    def setup_vertex_attribs(self) -> None:
        _POSITION = 0
        _COLOR = 1
        _SIZE_OF_GL_FLOAT = 4

        # Data
        vertices = self.model_element.get_vertices()
        indices = self.model_element.get_indices()
        values = self.model_element.get_values()

        self.vertices_size = vertices.size
        self.indices_size = indices.size
        self.values_size = values.size

        self.widget.makeCurrent()
        self.vao.bind()

        self.positions_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, _SIZE_OF_GL_FLOAT * self.vertices_size, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None)

        self.values_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, _SIZE_OF_GL_FLOAT * self.values_size, values, GL_STATIC_DRAW)
        glVertexAttribPointer(_COLOR, 3, GL_FLOAT, False, 0, None)

        self.indices_ibo.bind()
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(_POSITION)
        glEnableVertexAttribArray(_COLOR)

        self.vao.release()

    def setup_uniforms(self) -> None:
        pass

    def draw(self) -> None:
        pass

    """
    API for QTreeWidgetItem
    """
    def toggle_wireframe(self) -> bool:
        return False

    def update(self) -> None:
        self.widget.update()
