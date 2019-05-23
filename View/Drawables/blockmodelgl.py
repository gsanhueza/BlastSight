#!/usr/bin/env python

from View.Drawables.gldrawable import GLDrawable
from OpenGL.GL import *
from PyQt5.QtGui import QVector2D


class BlockModelGL(GLDrawable):
    def __init__(self, widget, element):
        super().__init__(widget, element)

        # Uniforms
        self.model_view_matrix_loc = None
        self.proj_matrix_loc = None
        self.block_size_loc = None

        # Block size
        self.block_size = 2.0

    def initialize(self) -> None:
        self.vertex_shader_source = 'View/Shaders/BlockModel/vertex.glsl'
        self.fragment_shader_source = 'View/Shaders/BlockModel/fragment.glsl'
        self.geometry_shader_source = 'View/Shaders/BlockModel/geometry.glsl'

        super().initialize()

    def initialize_shader_program(self) -> None:
        super().initialize_shader_program()

        self.shader_program.addShader(self.vertex_shader)
        self.shader_program.addShader(self.fragment_shader)
        self.shader_program.addShader(self.geometry_shader)
        self.shader_program.link()

    def setup_uniforms(self) -> None:
        self.model_view_matrix_loc = self.shader_program.uniformLocation('model_view_matrix')
        self.proj_matrix_loc = self.shader_program.uniformLocation('proj_matrix')
        self.block_size_loc = self.shader_program.uniformLocation('block_size')

    def setup_vertex_attribs(self) -> None:
        _POSITION = 0
        _COLOR = 1
        _SIZE_OF_GL_FLOAT = 4

        # Data
        vertices = self.element.vertices
        values = self.element.values

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

    def draw(self, proj_matrix, view_matrix, model_matrix) -> None:
        if not self.is_visible:
            return

        self.shader_program.bind()
        self.shader_program.setUniformValue(self.proj_matrix_loc, proj_matrix)
        self.shader_program.setUniformValue(self.model_view_matrix_loc, view_matrix * model_matrix)
        self.shader_program.setUniformValue(self.block_size_loc, QVector2D(self.block_size, 0.0))

        self.vao.bind()

        # np.array([[0, 1, 2]], type) has size 3, despite having only 1 list there
        glEnable(GL_PROGRAM_POINT_SIZE)
        glDrawArrays(GL_POINTS, 0, self.vertices_size // 3)

        self.vao.release()
