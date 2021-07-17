#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import freetype
import numpy as np

from OpenGL.GL import *
from .gldrawable import GLDrawable
from ..glprograms.textprogram import TextProgram


class TextGL(GLDrawable):
    fontfile = r'/usr/share/fonts/TTF/cour.ttf'
    characters = {}

    try:
        face = freetype.Face(fontfile)
    except freetype.ft_errors.FT_Exception:
        fontfile = r'C:\Windows\Fonts\cour.ttf'
        face = freetype.Face(fontfile)

    def __init__(self, element, *args, **kwargs):
        super().__init__(element, *args, **kwargs)
        self.text_vertices = []
        self.vertices = np.empty(3)

        self.text = kwargs.get('text', ' ')
        self.scale = kwargs.get('scale', 0.1)
        self.position = kwargs.get('position', [0.0, 0.0, 0.0])
        self.orientation = kwargs.get('orientation', 'elevation')

        # Set character size
        self.face.set_char_size(48 * 64)

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
    def _rendering_buffer_elevation(xpos, ypos, zpos, w, h) -> np.ndarray:
        return np.asarray([
            xpos,     ypos + h, zpos,
            xpos,     ypos,     zpos,
            xpos + w, ypos,     zpos,
            xpos,     ypos + h, zpos,
            xpos + w, ypos,     zpos,
            xpos + w, ypos + h, zpos,
        ], np.float32)

    @staticmethod
    def _rendering_buffer_north(xpos, ypos, zpos, w, h) -> np.ndarray:
        return np.asarray([
            xpos,     ypos,     zpos + h,
            xpos,     ypos,     zpos,
            xpos,     ypos + w, zpos,
            xpos,     ypos,     zpos + h,
            xpos,     ypos + w, zpos,
            xpos,     ypos + w, zpos + h,
        ], np.float32)

    @staticmethod
    def _rendering_buffer_east(xpos, ypos, zpos, w, h) -> np.ndarray:
        return np.asarray([
            xpos,     ypos,     zpos + h,
            xpos,     ypos,     zpos,
            xpos + w, ypos,     zpos,
            xpos,     ypos,     zpos + h,
            xpos + w, ypos,     zpos,
            xpos + w, ypos,     zpos + h,
        ], np.float32)

    @staticmethod
    def _get_rendering_texture() -> np.ndarray:
        return np.asarray([
            0, 0,
            0, 1,
            1, 1,
            0, 0,
            1, 1,
            1, 0,
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

        # Offset
        for i in range(len(self.text_vertices)):
            self.text_vertices[i] = self.text_vertices[i].reshape((-1, 3)).astype(np.float32)

    def generate_buffers(self) -> None:
        self._vaos = [glGenVertexArrays(1)]
        self._vbos = glGenBuffers(2)

    def setup_attributes(self) -> None:
        _POSITION = 0
        _TEXTURE = 1

        # Disable byte-alignment restriction
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        # Fill buffer (with empty data for now)
        glBindVertexArray(self.vao)
        self.fill_buffer(_POSITION, 3, np.zeros(6 * 3), GLfloat, GL_FLOAT, self._vbos[_POSITION])
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
            glDrawArrays(GL_TRIANGLES, 0, 6)

        glBindVertexArray(0)
        glBindTexture(GL_TEXTURE_2D, 0)
