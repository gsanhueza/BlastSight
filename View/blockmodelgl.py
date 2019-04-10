#!/usr/bin/env python

from View.gldrawable import GLDrawable
from OpenGL.GL import *
from PySide2.QtGui import QVector2D


class BlockModelGL(GLDrawable):
    def __init__(self, opengl_widget):
        super().__init__(opengl_widget)

        # Uniforms
        self.model_view_matrix_loc = None
        self.proj_matrix_loc = None
        self.block_size_loc = None

        # Block size
        self.block_size = 0.5

    def initialize(self):
        self.set_vertex_shader_source('View/Shaders/block_model_vertex.glsl')
        self.set_fragment_shader_source('View/Shaders/block_model_fragment.glsl')
        self.set_geometry_shader_source('View/Shaders/block_model_geometry.glsl')

        super().initialize()

    def setup_uniforms(self):
        self.model_view_matrix_loc = self.shader_program.uniformLocation('model_view_matrix')
        self.proj_matrix_loc = self.shader_program.uniformLocation('proj_matrix')
        self.block_size_loc = self.shader_program.uniformLocation('block_size')

    def draw(self):
        self.shader_program.bind()
        self.shader_program.setUniformValue(self.proj_matrix_loc, self.widget.proj)
        self.shader_program.setUniformValue(self.model_view_matrix_loc, self.widget.camera * self.widget.world)
        self.shader_program.setUniformValue(self.block_size_loc, QVector2D(self.block_size, 0.0))

        self.vao.bind()

        glDrawElements(GL_POINTS, self.indices.size, GL_UNSIGNED_INT, None)

        self.vao.release()