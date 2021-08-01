#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import freetype

from OpenGL.GL import *
from .shaderprogram import ShaderProgram


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


class TextProgram(ShaderProgram):
    # Static attributes
    characters = {}

    try:
        fontfile = r'/usr/share/fonts/TTF/cour.ttf'
        face = freetype.Face(fontfile)
    except freetype.ft_errors.FT_Exception:
        fontfile = r'C:\Windows\Fonts\cour.ttf'
        face = freetype.Face(fontfile)

    # Set character size
    face.set_char_size(48 * 64)

    def __init__(self):
        super().__init__()
        self.base_name = 'Text'

    def initialize(self) -> None:
        super().initialize()
        self.setup_characters()

    @classmethod
    def setup_characters(cls) -> None:
        # Disable byte-alignment restriction
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        for char in map(chr, range(0, 128)):
            cls.face.load_char(char)
            glyph = cls.face.glyph

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
            cls.characters[char] = CharacterSlot(texture, glyph)

            glBindTexture(GL_TEXTURE_2D, 0)
