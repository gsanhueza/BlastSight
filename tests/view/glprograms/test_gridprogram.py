#!/usr/bin/env python

from blastsight.view.drawables.gridgl import GridGL
from blastsight.view.glprograms.gridprogram import GridProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestGridProgram(TestShaderProgram):
    @property
    def base_program(self):
        return GridProgram()

    @property
    def base_drawable(self):
        return GridGL(self.base_element)
