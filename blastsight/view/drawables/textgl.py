#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import freetype
import numpy as np

from OpenGL.GL import *
from .gldrawable import GLDrawable
from ...model.elements.nullelement import NullElement


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
    def __init__(self, element=None, *args, **kwargs):
        super().__init__(NullElement(*args, **kwargs), *args, **kwargs)
        self.fontfile = r'/usr/share/fonts/gnu-free/FreeMono.otf'
        self.face = freetype.Face(self.fontfile)
        self.characters = {}
        self.text_vertices = []

        self.text = kwargs.get('text', ' ')
        self.scale = kwargs.get('scale', 1)
        self.vertices = [kwargs.get('position', [0.0, 0.0, 0.0])]

    @staticmethod
    def _get_rendering_buffer(xpos, ypos, zpos, w, h) -> np.ndarray:
        return np.asarray([
            xpos,     ypos + h, zpos,
            xpos,     ypos,     zpos,
            xpos + w, ypos,     zpos,
            xpos,     ypos + h, zpos,
            xpos + w, ypos,     zpos,
            xpos + w, ypos + h, zpos,
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
        # Retrieve positions
        x = self.x[0]
        y = self.y[0]
        z = self.z[0]

        for c in self.text:
            ch = self.characters[c]
            w, h = ch.textureSize
            w = w * self.scale
            h = h * self.scale
            self.text_vertices.append(self._get_rendering_buffer(x, y, z, w, h))

            # Now advance cursors for next glyph (note that advance is number of 1/64 pixels)
            x += (ch.advance >> 6) * self.scale

    def setup_attributes(self) -> None:
        _POSITION = 0
        _TEXTURE = 1

        # Disable byte-alignment restriction
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        # Set character size
        self.face.set_char_size(48 * 64)

        # Load first 128 characters of ASCII set
        self._setup_characters()

        # Setup text vertices
        self._setup_text_vertices()

        # Generate VAO and VBOs (see GLDrawable)
        self.generate_buffers(2)
        glBindVertexArray(self.vao)

        # Fill buffer (with empty data for now)
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

    @property
    def bounding_box(self):
        if not bool(self.characters):
            print(f'{self} characters have not been generated yet!')
            return self.vertices[0], self.vertices[0]

        self.vertices = np.unique(np.array(self.text_vertices).flatten().reshape((-1, 3)), axis=0)
        return self.element.bounding_box
