#!/usr/bin/env python

from View.Drawables.gldrawable import GLDrawable
from OpenGL.GL import *
from PyQt5.QtGui import QVector2D


class BlockModelGL(GLDrawable):
    def __init__(self, opengl_widget, model_element):
        super().__init__(opengl_widget, model_element)

        # Uniforms
        self.model_view_matrix_loc = None
        self.proj_matrix_loc = None
        self.block_size_loc = None

        # Block size
        self.block_size = 2.0

    def initialize(self) -> None:
        self.set_vertex_shader_source('View/Shaders/BlockModel/vertex.glsl')
        self.set_fragment_shader_source('View/Shaders/BlockModel/fragment.glsl')
        self.set_geometry_shader_source('View/Shaders/BlockModel/geometry.glsl')

        super().initialize()

    def setup_uniforms(self) -> None:
        self.model_view_matrix_loc = self.shader_program.uniformLocation('model_view_matrix')
        self.proj_matrix_loc = self.shader_program.uniformLocation('proj_matrix')
        self.block_size_loc = self.shader_program.uniformLocation('block_size')

    def setup_vertex_attribs(self) -> None:
        _POSITION = 0
        _COLOR = 1
        _SIZE_OF_GL_FLOAT = 4

        # Data
        vertices = self.model_element.get_vertices()
        values = self.model_element.get_values()

        self.vertices_size = vertices.size
        self.values_size = values.size

        self.widget.makeCurrent()
        self.vao.bind()

        self.vertices_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, _SIZE_OF_GL_FLOAT * self.vertices_size, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None)

        self.values_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, _SIZE_OF_GL_FLOAT * self.values_size, values, GL_STATIC_DRAW)
        glVertexAttribPointer(_COLOR, 3, GL_FLOAT, False, 0, None)

        glEnableVertexAttribArray(_POSITION)
        glEnableVertexAttribArray(_COLOR)

        self.vao.release()

    def draw(self) -> None:
        if not self.is_visible:
            return

        self.shader_program.bind()
        self.shader_program.setUniformValue(self.proj_matrix_loc, self.widget.proj)
        self.shader_program.setUniformValue(self.model_view_matrix_loc, self.widget.camera * self.widget.world)
        self.shader_program.setUniformValue(self.block_size_loc, QVector2D(self.block_size, 0.0))

        self.vao.bind()

        # np.array([[0, 1, 2]], type) has size 3, despite the 1 list there
        glDrawArrays(GL_POINTS, 0, self.vertices_size // 3)

        self.vao.release()
