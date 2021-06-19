#!/usr/bin/env python

from blastsight.view.drawables.backgroundgl import BackgroundGL
from blastsight.view.glprograms.backgroundprogram import BackgroundProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestBackgroundProgram(TestShaderProgram):
    @property
    def base_program(self):
        return BackgroundProgram()

    @property
    def base_drawable(self):
        return BackgroundGL(self.base_element)
