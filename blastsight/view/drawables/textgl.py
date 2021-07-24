#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np

from OpenGL.GL import *
from .gldrawable import GLDrawable
from ..glprograms.textprogram import TextProgram


class TextGL(GLDrawable):
    def __init__(self, element, *args, **kwargs):
        super().__init__(element, *args, **kwargs)
        self.text_vertices = []
        self.vertices = np.empty(3)

        self.text = kwargs.get('text', ' ')
        self.scale = kwargs.get('scale', 0.1)
        self.position = kwargs.get('position', [0.0, 0.0, 0.0])
        self.orientation = kwargs.get('orientation', 'elevation')

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

    @staticmethod
    def _rendering_buffer(xpos, ypos, zpos) -> np.ndarray:
        return np.asarray(4 * [xpos, ypos, zpos], np.float32)

    @classmethod
    def _rendering_buffer_elevation(cls, xpos, ypos, zpos, w, h) -> np.ndarray:
        return cls._rendering_buffer(xpos, ypos, zpos) + np.asarray([
            0, h, 0,
            0, 0, 0,
            w, h, 0,
            w, 0, 0,
        ], np.float32)

    @classmethod
    def _rendering_buffer_north(cls, xpos, ypos, zpos, w, h) -> np.ndarray:
        return cls._rendering_buffer(xpos, ypos, zpos) + np.array([
            0, 0, h,
            0, 0, 0,
            0, w, h,
            0, w, 0,
        ], np.float32)

    @classmethod
    def _rendering_buffer_east(cls, xpos, ypos, zpos, w, h) -> np.ndarray:
        return cls._rendering_buffer(xpos, ypos, zpos) + np.asarray([
            0, 0, h,
            0, 0, 0,
            w, 0, h,
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
        self.text_vertices.clear()

        # Retrieve positions
        x, y, z = self.position

        for c in self.text:
            ch = TextProgram.characters[c]
            w, h = ch.textureSize
            w = w * self.scale
            h = h * self.scale

            # Select best vertices using orientation
            if self.orientation == 'elevation':
                self.text_vertices.append(self._rendering_buffer_elevation(x, y, z, w, h))
                x += (ch.advance >> 6) * self.scale

            elif self.orientation == 'north':
                self.text_vertices.append(self._rendering_buffer_north(x, y, z, w, h))
                y += (ch.advance >> 6) * self.scale

            else:  # if self.orientation == 'east':
                self.text_vertices.append(self._rendering_buffer_east(x, y, z, w, h))
                x += (ch.advance >> 6) * self.scale

    def generate_buffers(self) -> None:
        self._vaos = [glGenVertexArrays(1)]
        self._vbos = glGenBuffers(2)

    def setup_attributes(self) -> None:
        _POSITION = 0
        _TEXTURE = 1

        # Fill buffer (with empty data for now)
        glBindVertexArray(self.vao)
        self.fill_buffer(_POSITION, 3, np.zeros(4 * 3), GLfloat, GL_FLOAT, self._vbos[_POSITION])
        self.fill_buffer(_TEXTURE, 2, self._get_rendering_texture(), GLfloat, GL_FLOAT, self._vbos[_TEXTURE])
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        glBindVertexArray(0)

    def draw(self) -> None:
        glActiveTexture(GL_TEXTURE0)
        glBindVertexArray(self.vao)

        for i, c in enumerate(self.text):
            ch = TextProgram.characters[c]
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
