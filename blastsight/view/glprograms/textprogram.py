#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from OpenGL.GL import *
from .shaderprogram import ShaderProgram
from ..glprograms.text_management.textmanager import TextManager


class TextProgram(ShaderProgram):
    def __init__(self):
        super().__init__()
        self.base_name = 'Text'

    def initialize(self) -> None:
        super().initialize()
        TextManager.setup_characters()

    def draw(self) -> None:
        glDepthMask(GL_FALSE)
        super().draw()
        glDepthMask(GL_TRUE)
