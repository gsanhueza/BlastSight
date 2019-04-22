#!/usr/bin/env python

from View.gldrawable import GLDrawable
from OpenGL.GL import *


class MeshGL(GLDrawable):
    def __init__(self, opengl_widget, model_element):
        super().__init__(opengl_widget, model_element)

        # Uniforms
        self.model_view_matrix_loc = None
        self.proj_matrix_loc = None

        # Wireframe
        self.wireframe_enabled = True

    def initialize(self) -> None:
        self.set_vertex_shader_source('View/Shaders/Mesh/vertex.glsl')
        self.set_fragment_shader_source('View/Shaders/Mesh/fragment.glsl')
        # self.set_geometry_shader_source('View/Shaders/Mesh/geometry_wireframe.glsl')
        self.set_geometry_shader_source('View/Shaders/Mesh/geometry_normals.glsl')

        super().initialize()

    def setup_uniforms(self):
        self.model_view_matrix_loc = self.shader_program.uniformLocation('model_view_matrix')
        self.proj_matrix_loc = self.shader_program.uniformLocation('proj_matrix')

    def toggle_wireframe(self) -> bool:
        if self.wireframe_enabled:
            self.shader_program.removeShader(self.geometry_shader)
            self.wireframe_enabled = False
        else:
            self.shader_program.addShader(self.geometry_shader)
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
