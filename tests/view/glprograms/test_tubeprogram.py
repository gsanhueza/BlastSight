#!/usr/bin/env python

from blastsight.model.elements.tubeelement import TubeElement
from blastsight.view.drawables.tubegl import TubeGL
from blastsight.view.glprograms.tubeprogram import TubeProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestTubeProgram(TestShaderProgram):
    @property
    def base_program(self):
        return TubeProgram()

    @property
    def base_element(self):
        return TubeElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0])

    @property
    def base_drawable(self):
        return TubeGL(self.base_element)
