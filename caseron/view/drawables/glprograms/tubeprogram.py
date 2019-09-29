#!/usr/bin/env python

from .shaderprogram import ShaderProgram


class TubeProgram(ShaderProgram):
    def __init__(self, widget):
        super().__init__(widget)
        self.base_name = 'Tube'