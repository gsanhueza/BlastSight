#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np
from qtpy.QtGui import QMatrix4x4, QVector3D

from OpenGL.GL import *
from .gldrawable import GLDrawable
from ..glprograms.text_management.textmanager import TextManager


class TextGL(GLDrawable):
    def __init__(self, element, *args, **kwargs):
        super().__init__(element, *args, **kwargs)
        self.text_vertices = []
        self.vertices = np.empty(3)

        self._position = kwargs.get('position', np.zeros(3))
        self._color = kwargs.get('color', np.ones(3))

        self.text = kwargs.get('text', ' ')
        self.scale = kwargs.get('scale', 1.0)

        self.rotation = kwargs.get('rotation', np.zeros(3))
        self.centered = kwargs.get('centered', False)

    @property
    def position(self) -> np.array:
        return np.asarray(self._position, np.float32)

    @position.setter
    def position(self, value: iter) -> None:
        self._position = np.array(value, np.float32)

    @property
    def color(self) -> np.array:
        return np.asarray(self._color, np.float32)

    @color.setter
    def color(self, value: iter) -> None:
        self._color = np.array(value, np.float32)

    def initialize(self) -> None:
        if self.is_initialized:
            return

        self.initialize_textures()
        super().initialize()

    def initialize_textures(self) -> None:
        # Setup text vertices
        self._setup_text_vertices()

        # Now we can update the real vertices
        self.vertices = np.unique(np.array(self.text_vertices).flatten().reshape((-1, 3)), axis=0)

    @property
    def tex_scale(self) -> float:
        return self.scale / 48

    @classmethod
    def _rendering_buffer(cls, xpos, ypos, zpos, w, h) -> np.ndarray:
        return np.asarray(4 * [xpos, ypos, zpos], np.float32) + np.asarray([
            0, h, 0,
            0, 0, 0,
            w, h, 0,
            w, 0, 0,
        ], np.float32)

    @classmethod
    def _get_rendering_texture(cls) -> np.ndarray:
        return np.asarray([
            0, 0,
            0, 1,
            1, 0,
            1, 1,
        ], np.float32)

    def _setup_text_vertices(self) -> None:
        text_vertices = []

        # Retrieve initial position
        x, y, z = self.position

        # Setup text vertices
        for c in self.text:
            ch = TextManager.characters[c]
            w, h = ch.textureSize
            w = w * self.tex_scale
            h = h * self.tex_scale

            text_vertices.append(self._rendering_buffer(x, y, z, w, h))
            x += (ch.advance >> 6) * self.tex_scale

        tvs = np.array(text_vertices).reshape((-1, 3))

        # Rotate vertices as required
        matrix = QMatrix4x4()

        matrix.translate(*self.position)
        matrix.rotate(self.rotation[0], 1.0, 0.0, 0.0)
        matrix.rotate(self.rotation[1], 0.0, 1.0, 0.0)
        matrix.rotate(self.rotation[2], 0.0, 0.0, 1.0)
        matrix.translate(*-self.position)

        # PySide2 requires this workaround
        tvs_response = []

        for vec in tvs:
            vec4 = vec.tolist() + [1.0]
            temp_matrix = QMatrix4x4(*4 * vec4)

            response = (matrix * temp_matrix.transposed()).column(0)
            np_response = np.array([response.x(), response.y(), response.z()], np.float32)

            tvs_response.append(np_response)

        tvs = np.array(tvs_response, np.float32).reshape((len(self.text), -1))

        # Centered = Position represents center of the whole text, instead of the bottom left.
        if self.centered:
            ptp = np.ptp(tvs, axis=0)
            tvs -= ptp / 2

        self.text_vertices = tvs.reshape((len(self.text), -1))

    def generate_buffers(self) -> None:
        self._vaos = [glGenVertexArrays(1)]
        self._vbos = glGenBuffers(3)

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1
        _TEXTURE = 2

        # Fill buffer (with empty data for now)
        glBindVertexArray(self.vao)
        self.fill_buffer(_POSITION, 3, np.zeros(4 * 3), GLfloat, GL_FLOAT, self._vbos[_POSITION])
        self.fill_buffer(_COLOR, 3, self.color, GLfloat, GL_FLOAT, self._vbos[_COLOR])
        self.fill_buffer(_TEXTURE, 2, self._get_rendering_texture(), GLfloat, GL_FLOAT, self._vbos[_TEXTURE])
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        # Distribute along the whole instance
        glVertexAttribDivisor(_COLOR, 1)

        glBindVertexArray(0)

    def draw(self) -> None:
        glActiveTexture(GL_TEXTURE0)
        glBindVertexArray(self.vao)

        for i, c in enumerate(self.text):
            ch = TextManager.characters[c]
            vertices = self.text_vertices[i]

            # Render glyph texture over quad
            glBindTexture(GL_TEXTURE_2D, ch.texture)

            # Update content of VBO memory
            glBindBuffer(GL_ARRAY_BUFFER, self._vbos[0])
            glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)
            glBindBuffer(GL_ARRAY_BUFFER, 0)

            # Render quad
            glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

        glBindTexture(GL_TEXTURE_2D, 0)
        glBindVertexArray(0)
