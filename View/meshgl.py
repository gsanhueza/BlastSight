#!/usr/bin/env python

from View.gldrawable import GLDrawable
from OpenGL.GL import *


class MeshGL(GLDrawable):
    def __init__(self, opengl_widget):
        super().__init__(opengl_widget)

        # Uniforms
        self.model_view_matrix_loc = None
        self.proj_matrix_loc = None

        # Wireframe
        self.wireframe_enabled = True

    def setup_uniforms(self):
        self.model_view_matrix_loc = self.shader_program.uniformLocation('model_view_matrix')
        self.proj_matrix_loc = self.shader_program.uniformLocation('proj_matrix')

    def toggle_wireframe(self):
        if self.wireframe_enabled:
            self.shader_program.removeShader(self.geometry_shader)
            self.wireframe_enabled = False
        else:
            self.shader_program.addShader(self.geometry_shader)
            self.wireframe_enabled = True

    def draw(self):
        self.shader_program.bind()
        self.shader_program.setUniformValue(self.proj_matrix_loc, self.widget.proj)
        self.shader_program.setUniformValue(self.model_view_matrix_loc, self.widget.camera * self.widget.world)

        self.vao.bind()

        glDrawElements(GL_TRIANGLES, self.indices.size, GL_UNSIGNED_INT, None)

        self.vao.release()
