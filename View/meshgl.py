#!/usr/bin/env python

from PyQt5.QtGui import QOpenGLShader
from View.gldrawable import GLDrawable
from OpenGL.GL import *


class MeshGL(GLDrawable):
    def __init__(self, opengl_widget, model_element):
        super().__init__(opengl_widget, model_element)

        # Uniforms
        self.model_view_matrix_loc = None
        self.proj_matrix_loc = None

        # Wireframe
        self.wireframe_enabled = False

        # Extra shaders
        self.fragment_wireframe_shader = None
        self.geometry_wireframe_shader = None

    def initialize_shader_program(self) -> None:
        self.vertex_shader = QOpenGLShader(QOpenGLShader.Vertex)
        self.fragment_shader = QOpenGLShader(QOpenGLShader.Fragment)
        self.geometry_shader = QOpenGLShader(QOpenGLShader.Geometry)

        self.vertex_shader.compileSourceFile(self.vertex_shader_source)
        self.fragment_shader.compileSourceFile(self.fragment_shader_source)
        self.geometry_shader.compileSourceFile(self.geometry_shader_source)

        # Extra shaders
        self.fragment_wireframe_shader = QOpenGLShader(QOpenGLShader.Fragment)
        self.fragment_wireframe_shader.compileSourceFile('View/Shaders/Mesh/fragment_wireframe.glsl')
        self.geometry_wireframe_shader = QOpenGLShader(QOpenGLShader.Geometry)
        self.geometry_wireframe_shader.compileSourceFile('View/Shaders/Mesh/geometry_wireframe.glsl')

        self.shader_program.addShader(self.vertex_shader)
        self.shader_program.addShader(self.fragment_shader)
        self.shader_program.addShader(self.geometry_shader)
        self.shader_program.link()

    def initialize(self) -> None:
        self.set_vertex_shader_source('View/Shaders/Mesh/vertex.glsl')
        self.set_fragment_shader_source('View/Shaders/Mesh/fragment_normals.glsl')
        self.set_geometry_shader_source('View/Shaders/Mesh/geometry_normals.glsl')

        super().initialize()

    def setup_uniforms(self) -> None:
        self.model_view_matrix_loc = self.shader_program.uniformLocation('model_view_matrix')
        self.proj_matrix_loc = self.shader_program.uniformLocation('proj_matrix')

    def toggle_wireframe(self) -> bool:
        if self.wireframe_enabled:
            self.shader_program.removeShader(self.geometry_wireframe_shader)
            self.shader_program.removeShader(self.fragment_wireframe_shader)
            self.shader_program.addShader(self.geometry_shader)
            self.shader_program.addShader(self.fragment_shader)
            self.wireframe_enabled = False
        else:
            self.shader_program.removeShader(self.geometry_shader)
            self.shader_program.removeShader(self.fragment_shader)
            self.shader_program.addShader(self.geometry_wireframe_shader)
            self.shader_program.addShader(self.fragment_wireframe_shader)
            self.wireframe_enabled = True
        return self.wireframe_enabled

    def draw(self) -> None:
        if not self.is_visible:
            return

        self.shader_program.bind()
        self.shader_program.setUniformValue(self.proj_matrix_loc, self.widget.proj)
        self.shader_program.setUniformValue(self.model_view_matrix_loc, self.widget.camera * self.widget.world)

        self.vao.bind()
        glDrawElements(GL_TRIANGLES, self.indices_size, GL_UNSIGNED_INT, None)
        self.vao.release()
