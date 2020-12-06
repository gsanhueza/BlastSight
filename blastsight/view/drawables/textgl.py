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
        self.fontfile = r'/usr/share/fonts/gnu-free/FreeMono.otf'

        self.face = freetype.Face(self.fontfile)
        self.characters = {}

    @staticmethod
    def _get_rendering_buffer(xpos, ypos, w, h, zfix=0.0):
        return np.asarray([
            xpos,     ypos + h, 0, 0,
            xpos,     ypos,     0, 1,
            xpos + w, ypos,     1, 1,
            xpos,     ypos + h, 0, 0,
            xpos + w, ypos,     1, 1,
            xpos + w, ypos + h, 1, 0,
        ], np.float32)

    def setup_attributes(self) -> None:
        _POSITION = 0

        # Disable byte-alignment restriction
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        self.face.set_char_size(48 * 64)

        # load first 128 characters of ASCII set
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

        # Generate VAO and VBOs (see GLDrawable)
        self.generate_buffers(1)
        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self._vbos)
        glBufferData(GL_ARRAY_BUFFER, 6 * 4 * 4, None, GL_DYNAMIC_DRAW)
        glEnableVertexAttribArray(_POSITION)
        glVertexAttribPointer(_POSITION, 4, GL_FLOAT, GL_FALSE, 0, None)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def draw(self) -> None:
        glActiveTexture(GL_TEXTURE0)
        glBindVertexArray(self.vao)

        # FIXME Extract these from the drawable, instead of hard-coding them
        text = "hello"
        scale = 1
        x = 20
        y = 50

        for c in text:
            ch = self.characters[c]
            w, h = ch.textureSize
            w = w * scale
            h = h * scale
            vertices = self._get_rendering_buffer(x, y, w, h)

            # render glyph texture over quad
            glBindTexture(GL_TEXTURE_2D, ch.texture)
            # update content of VBO memory
            glBindBuffer(GL_ARRAY_BUFFER, self._vbos)
            glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)

            glBindBuffer(GL_ARRAY_BUFFER, 0)
            # render quad
            glDrawArrays(GL_TRIANGLES, 0, 6)
            # now advance cursors for next glyph (note that advance is number of 1/64 pixels)
            x += (ch.advance >> 6) * scale

        glBindVertexArray(0)
        glBindTexture(GL_TEXTURE_2D, 0)
