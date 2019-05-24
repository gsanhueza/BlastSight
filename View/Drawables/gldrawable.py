#!/usr/bin/env python

from PyQt5.QtGui import QOpenGLShaderProgram
from PyQt5.QtGui import QOpenGLVertexArrayObject
from PyQt5.QtGui import QOpenGLShader


class GLDrawable:
    def __init__(self, widget, element):
        assert widget
        assert element
        self._widget = widget
        self._element = element

        # Shader program
        self.shader_program = None

        # Vertex Array Object
        self.vao = None

        self.is_initialized = False
        self.is_visible = True

        # Sizes
        self.vertices_size = 0
        self.indices_size = 0
        self.values_size = 0

    @property
    def id(self):
        return self._element.id

    @id.setter
    def id(self, _id):
        self._element.id = _id

    @property
    def widget(self):
        return self._widget

    @property
    def element(self):
        return self._element

    def show(self) -> None:
        self.is_visible = True

    def hide(self) -> None:
        self.is_visible = False

    def initialize(self) -> None:
        self.initialize_program()
        self.initialize_shaders()
        self.setup_attributes()
        self.setup_uniforms()

        self.is_initialized = True

    def initialize_program(self) -> None:
        self.shader_program = QOpenGLShaderProgram(self.widget.context())
        self.vao = QOpenGLVertexArrayObject()
        self.vao.create()

    def initialize_shaders(self) -> None:
        # Remember to set shader sources in children of this class
        # For example:

        # self.vertex_shader = QOpenGLShader(QOpenGLShader.Vertex)
        # self.fragment_shader = QOpenGLShader(QOpenGLShader.Fragment)
        # self.geometry_shader = QOpenGLShader(QOpenGLShader.Geometry)

        # self.vertex_shader_source = 'View/Shaders/mesh_vertex.glsl'
        # self.fragment_shader_source = 'View/Shaders/mesh_fragment.glsl'
        # self.geometry_shader_source = 'View/Shaders/mesh_geometry.glsl'

        # self.vertex_shader.compileSourceFile(self.vertex_shader_source)
        # self.fragment_shader.compileSourceFile(self.fragment_shader_source)
        # self.geometry_shader.compileSourceFile(self.geometry_shader_source)
        #
        # self.shader_program.addShader(self.vertex_shader)
        # self.shader_program.addShader(self.fragment_shader)
        # self.shader_program.addShader(self.geometry_shader)
        # self.shader_program.link()
        pass

    def setup_attributes(self) -> None:
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
