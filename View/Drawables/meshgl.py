#!/usr/bin/env python

from PyQt5.QtGui import QOpenGLBuffer
from PyQt5.QtGui import QOpenGLShader
from PyQt5.QtGui import QOpenGLShaderProgram
from PyQt5.QtGui import QOpenGLVertexArrayObject
from PyQt5.QtGui import QVector2D
from PyQt5.QtGui import QVector3D
from View.Drawables.gldrawable import GLDrawable
from OpenGL.GL import *


class MeshGL(GLDrawable):
    def __init__(self, widget=None, element=None):
        super().__init__(widget, element)

        # Uniforms
        self.model_view_matrix_loc = None
        self.proj_matrix_loc = None
        self.color_loc = None
        self.alpha_loc = None
        self.color = None
        self.alpha = None

        # Wireframe
        self.wireframe_enabled = False

        # Programs
        self.normal_program = None
        self.wireframe_program = None

    def initialize(self):
        super().initialize()
        self.update_wireframe()

    def initialize_program(self) -> None:
        self.normal_program = QOpenGLShaderProgram(self.widget.context())
        self.wireframe_program = QOpenGLShaderProgram(self.widget.context())

        self.vao = QOpenGLVertexArrayObject()
        self.vao.create()

    def initialize_shaders(self) -> None:
        vertex_shader = QOpenGLShader(QOpenGLShader.Vertex)
        fragment_shader = QOpenGLShader(QOpenGLShader.Fragment)
        fragment_wireframe_shader = QOpenGLShader(QOpenGLShader.Fragment)
        geometry_shader = QOpenGLShader(QOpenGLShader.Geometry)

        vertex_shader.compileSourceFile('View/Shaders/Mesh/vertex.glsl')
        fragment_shader.compileSourceFile('View/Shaders/Mesh/fragment.glsl')
        fragment_wireframe_shader.compileSourceFile('View/Shaders/Mesh/fragment_wireframe.glsl')
        geometry_shader.compileSourceFile('View/Shaders/Mesh/geometry.glsl')

        self.normal_program.addShader(vertex_shader)
        self.normal_program.addShader(fragment_shader)
        self.normal_program.link()

        self.wireframe_program.addShader(vertex_shader)
        self.wireframe_program.addShader(fragment_wireframe_shader)
        self.wireframe_program.addShader(geometry_shader)
        self.wireframe_program.link()

        self.shader_program = self.normal_program

    def setup_attributes(self) -> None:
        _POSITION = 0
        _SIZE_OF_GL_FLOAT = 4

        # VBO
        vertices_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        indices_ibo = QOpenGLBuffer(QOpenGLBuffer.IndexBuffer)
        values_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)

        vertices_vbo.create()
        indices_ibo.create()
        values_vbo.create()

        # Data
        vertices = self.element.vertices
        indices = self.element.indices

        self.vertices_size = vertices.size
        self.indices_size = indices.size

        self.widget.makeCurrent()
        self.vao.bind()

        vertices_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, _SIZE_OF_GL_FLOAT * self.vertices_size, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None)

        indices_ibo.bind()
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(_POSITION)

        self.vao.release()

    def setup_uniforms(self) -> None:
        self.model_view_matrix_loc = self.shader_program.uniformLocation('model_view_matrix')
        self.proj_matrix_loc = self.shader_program.uniformLocation('proj_matrix')
        self.color_loc = self.shader_program.uniformLocation('u_color')
        self.alpha_loc = self.shader_program.uniformLocation('u_alpha')

        color = list(self.element.values)
        self.color = QVector3D(color[0], color[1], color[2])

        alpha = 1.0  # self.model_element.get_alpha()
        self.alpha = QVector2D(alpha, 0.0)

    def update_wireframe(self) -> None:
        if self.shader_program:  # Will skip before viewer.show()
            if self.wireframe_enabled:
                self.enable_wireframe()
            else:
                self.disable_wireframe()

    def toggle_wireframe(self) -> bool:
        self.wireframe_enabled = not self.wireframe_enabled
        self.update_wireframe()
        return self.wireframe_enabled

    def disable_wireframe(self) -> None:
        self.shader_program = self.normal_program
        self.wireframe_enabled = False

    def enable_wireframe(self):
        self.shader_program = self.wireframe_program
        self.wireframe_enabled = True

    def draw(self, proj_matrix, view_matrix, model_matrix) -> None:
        if not self.is_visible:
            return

        self.shader_program.bind()
        self.shader_program.setUniformValue(self.proj_matrix_loc, proj_matrix)
        self.shader_program.setUniformValue(self.model_view_matrix_loc, view_matrix * model_matrix)
        self.shader_program.setUniformValue(self.color_loc, self.color)
        self.shader_program.setUniformValue(self.alpha_loc, self.alpha)
        self.vao.bind()
        glDrawElements(GL_TRIANGLES, self.indices_size, GL_UNSIGNED_INT, None)
        self.vao.release()
