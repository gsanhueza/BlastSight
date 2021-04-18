#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import freetype
import numpy as np

from OpenGL.GL import *
from .gldrawable import GLDrawable


# Adapted from https://stackoverflow.com/questions/63836707/how-to-render-text-with-pyopengl
class CharacterSlot:
    def __init__(self, texture, glyph):
        self.texture = texture
        self.textureSize = (glyph.bitmap.width, glyph.bitmap.rows)

        if isinstance(glyph, freetype.GlyphSlot):
            self.bearing = (glyph.bitmap_left, glyph.bitmap_top)
            self.advance = glyph.advance.x
        elif isinstance(glyph, freetype.BitmapGlyph):
            self.bearing = (glyph.left, glyph.top)
            self.advance = None
        else:
            raise RuntimeError('unknown glyph type')


class TextGL(GLDrawable):
    def __init__(self, element, *args, **kwargs):
        super().__init__(element, *args, **kwargs)
        self.fontfile = r'/usr/share/fonts/TTF/cour.ttf'

        try:
            self.face = freetype.Face(self.fontfile)
        except freetype.ft_errors.FT_Exception:
            self.fontfile = r'C:\Windows\Fonts\cour.ttf'
            self.face = freetype.Face(self.fontfile)

        self.characters = {}
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
        # Load first 128 characters of ASCII set
        self._setup_characters()

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

    def _setup_characters(self) -> None:
        for i in range(0, 128):
            self.face.load_char(chr(i))
            glyph = self.face.glyph

            # Generate texture
            texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, glyph.bitmap.width, glyph.bitmap.rows, 0,
                         GL_RED, GL_UNSIGNED_BYTE, glyph.bitmap.buffer)

            # Texture options
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            # Now store character for later use
            self.characters[chr(i)] = CharacterSlot(texture, glyph)

            glBindTexture(GL_TEXTURE_2D, 0)

    def _setup_text_vertices(self) -> None:
        self.text_vertices.clear()

        # Retrieve positions
        x, y, z = self.position

        for c in self.text:
            ch = self.characters[c]
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
            self.text_vertices[i] = (self.text_vertices[i].reshape((-1, 3)) + self.rendering_offset).astype(np.float32)

    def generate_buffers(self) -> None:
        self._vaos = [glGenVertexArrays(1)]
        self._vbos = glGenBuffers(2)

    def setup_attributes(self) -> None:
        _POSITION = 0
        _TEXTURE = 1

        # Disable byte-alignment restriction
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        # Load first 128 characters of ASCII set
        # (Why do we have to setup this twice (once in the constructor)?)
        self._setup_characters()

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
            ch = self.characters[c]
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
