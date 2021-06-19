#!/usr/bin/env python

from blastsight.model.elements.lineelement import LineElement
from blastsight.view.drawables.linegl import LineGL
from blastsight.view.glprograms.lineprogram import LineProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestLineProgram(TestShaderProgram):
    @property
    def base_program(self):
        return LineProgram()

    @property
    def base_element(self):
        return LineElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0])

    @property
    def base_drawable(self):
        return LineGL(self.base_element)
