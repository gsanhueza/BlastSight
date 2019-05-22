#!/usr/bin/env python

from OpenGL.GL import *
from PyQt5.QtGui import QOpenGLShaderProgram
from PyQt5.QtGui import QOpenGLVertexArrayObject
from PyQt5.QtGui import QOpenGLBuffer
from PyQt5.QtGui import QOpenGLShader


class GLDrawable:
    def __init__(self, widget, element):
        self._widget = widget
        self._element = element
        self._id = element.id

        # Shaders
        self.shader_program = QOpenGLShaderProgram(self.widget.context())
        self.vertex_shader = None
        self.fragment_shader = None
        self.geometry_shader = None

        self._vertex_shader_source = None
        self._fragment_shader_source = None
        self._geometry_shader_source = None

        # Vertex {Array/Buffer} Objects
        self.vao = None
        self.vertices_vbo = None
        self.values_vbo = None
        self.indices_ibo = None

        self.is_initialized = False
        self.is_visible = True

        # Sizes
        self.vertices_size = 0
        self.indices_size = 0
        self.values_size = 0

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, _id):
        self._id = _id

    @property
    def widget(self):
        return self._widget

    @property
    def element(self):
        return self._element

    @property
    def vertex_shader_source(self):
        return self._vertex_shader_source

    @vertex_shader_source.setter
    def vertex_shader_source(self, source):
        self._vertex_shader_source = source

    @property
    def fragment_shader_source(self):
        return self._fragment_shader_source

    @fragment_shader_source.setter
    def fragment_shader_source(self, source):
        self._fragment_shader_source = source

    @property
    def geometry_shader_source(self):
        return self._geometry_shader_source

    @geometry_shader_source.setter
    def geometry_shader_source(self, source):
        self._geometry_shader_source = source

    def show(self) -> None:
        self.is_visible = True

    def hide(self) -> None:
        self.is_visible = False

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

    def initialize_shader_program(self) -> None:
        self.vertex_shader = QOpenGLShader(QOpenGLShader.Vertex)
        self.fragment_shader = QOpenGLShader(QOpenGLShader.Fragment)
        self.geometry_shader = QOpenGLShader(QOpenGLShader.Geometry)

        self.vertex_shader.compileSourceFile(self._vertex_shader_source)
        self.fragment_shader.compileSourceFile(self._fragment_shader_source)
        self.geometry_shader.compileSourceFile(self._geometry_shader_source)

        self.shader_program.addShader(self.vertex_shader)
        self.shader_program.addShader(self.fragment_shader)
        self.shader_program.addShader(self.geometry_shader)
        self.shader_program.link()

    def initialize_buffers(self) -> None:
        self.vao = QOpenGLVertexArrayObject()
        self.vertices_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self.indices_ibo = QOpenGLBuffer(QOpenGLBuffer.IndexBuffer)
        self.values_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)

        self.vao.create()
        self.vertices_vbo.create()
        self.indices_ibo.create()
        self.values_vbo.create()

    def setup_vertex_attribs(self) -> None:
        pass

    def setup_uniforms(self) -> None:
        pass

    def draw(self, proj_matrix, view_matrix, model_matrix) -> None:
        pass

    """
    API for QTreeWidgetItem
    """
    def toggle_wireframe(self) -> bool:
        return False
