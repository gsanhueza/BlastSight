#!/usr/bin/env python

import numpy as np
import colorsys
from functools import partial

from qtpy.QtGui import QOpenGLShaderProgram
from qtpy.QtGui import QOpenGLVertexArrayObject
from qtpy.QtGui import QVector2D
from qtpy.QtGui import QOpenGLBuffer
from qtpy.QtGui import QOpenGLShader

from .gldrawable import GLDrawable
from OpenGL.GL import *


class BlockModelGL(GLDrawable):
    def __init__(self, widget=None, element=None):
        super().__init__(widget, element)

        # Uniforms
        self.block_size_loc = None

        # Sizes
        self.vertices_size = 0
        self.values_size = 0

        # Block size
        self.block_size = 1.0

    def initialize_program(self) -> None:
        self.shader_program = QOpenGLShaderProgram(self.widget.context())
        self.vao = QOpenGLVertexArrayObject()
        self.vao.create()

    def initialize_shaders(self) -> None:
        vertex_shader = QOpenGLShader(QOpenGLShader.Vertex)
        fragment_shader = QOpenGLShader(QOpenGLShader.Fragment)
        vertex_shader.compileSourceFile(f'{self._shader_dir}/BlockModel/vertex.glsl')
        fragment_shader.compileSourceFile(f'{self._shader_dir}/BlockModel/fragment.glsl')

        self.shader_program.addShader(vertex_shader)
        self.shader_program.addShader(fragment_shader)
        self.shader_program.link()

    def setup_attributes(self) -> None:
        def normalize(min_val: float, max_val: float, x: float) -> float:
            return (x - min_val) / (max_val - min_val) if max_val != min_val else 0

        _POSITION = 0
        _COLOR = 1
        # _TEMPLATE = 2

        # VBO
        vertices_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        values_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        # template_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)

        vertices_vbo.create()
        values_vbo.create()
        # template_vbo.create()

        # Data
        # template = self.generate_cube(self.element.block_size)
        vertices = self.element.vertices
        values = self.element.values

        min_val = values.min() if values.size > 0 else 0.0
        max_val = values.max() if values.size > 0 else 1.0

        # norm_func = partial(partial(normalize, min_val), max_val)
        # normalized_values = np.vectorize(norm_func, otypes=[np.float32])(values)

        # WARNING colorsys.hsv_to_rgb returns a tuple. but np.vectorize doesn't accept it as tuple
        # hue[0/3, 1/3, 2/3, 3/3] == [red, green, blue, red]
        # values = np.array(list(map(lambda hue: colorsys.hsv_to_rgb(2 * hue / 3, 1.0, 1.0),
        #                            normalized_values)), np.float32)

        self.vertices_size = vertices.size
        self.values_size = values.size

        self.widget.makeCurrent()
        self.vao.bind()

        vertices_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * self.vertices_size, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None)

        values_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * self.values_size, values, GL_STATIC_DRAW)
        glVertexAttribPointer(_COLOR, 3, GL_FLOAT, False, 0, None)

        # template_vbo.bind()
        # glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * template.size, template, GL_STATIC_DRAW)
        # glVertexAttribPointer(_TEMPLATE, 3, GL_FLOAT, False, 0, None)

        # glVertexAttribDivisor(_POSITION, 1)
        # glVertexAttribDivisor(_COLOR, 1)
        # glVertexAttribDivisor(_TEMPLATE, 0)

        glEnableVertexAttribArray(_POSITION)
        glEnableVertexAttribArray(_COLOR)
        # glEnableVertexAttribArray(_TEMPLATE)

        self.vao.release()

    def setup_uniforms(self) -> None:
        self.model_view_matrix_loc = self.shader_program.uniformLocation('model_view_matrix')
        self.proj_matrix_loc = self.shader_program.uniformLocation('proj_matrix')
        self.block_size_loc = self.shader_program.uniformLocation('block_size')

    def draw(self, proj_matrix=None, view_matrix=None, model_matrix=None):
        if not self.is_visible:
            return

        self.shader_program.bind()
        self.shader_program.setUniformValue(self.proj_matrix_loc, proj_matrix)
        self.shader_program.setUniformValue(self.model_view_matrix_loc, view_matrix * model_matrix)
        self.shader_program.setUniformValue(self.block_size_loc, QVector2D(self.block_size, 0.0))

        self.vao.bind()

        # np.array([[0, 1, 2]], type) has size 3, despite having only 1 list there
        # glDrawArraysInstanced(GL_TRIANGLE_STRIP, 0, 14, self.vertices_size // 3)
        glDrawArrays(GL_POINTS, 0, self.vertices_size // 3)

        self.vao.release()

    # Taken from https://stackoverflow.com/questions/28375338/cube-using-single-gl-triangle-strip
    @staticmethod
    def generate_cube(size: np.ndarray) -> np.ndarray:
        size_x = size[0] / 2
        size_y = size[1] / 2
        size_z = size[2] / 2

        cube_strip = [
            -size_x, size_y, size_z,  # Front-top-left
            size_x, size_y, size_z,  # Front-top-right
            -size_x, -size_y, size_z,  # Front-bottom-left
            size_x, -size_y, size_z,  # Front-bottom-right
            size_x, -size_y, -size_z,  # Back-bottom-right
            size_x, size_y, size_z,  # Front-top-right
            size_x, size_y, -size_z,  # Back-top-right
            -size_x, size_y, size_z,  # Front-top-left
            -size_x, size_y, -size_z,  # Back-top-left
            -size_x, -size_y, size_z,  # Front-bottom-left
            -size_x, -size_y, -size_z,  # Back-bottom-left
            size_x, -size_y, -size_z,  # Back-bottom-right
            -size_x, size_y, -size_z,  # Back-top-left
            size_x, size_y, -size_z,  # Back-top-right
        ]

        return np.array(cube_strip, np.float32)
