#!/usr/bin/env python

from blastsight.model.elements.pointelement import PointElement
from blastsight.view.drawables.pointgl import PointGL
from blastsight.view.glprograms.pointprogram import PointProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestPointProgram(TestShaderProgram):
    @property
    def base_program(self):
        return PointProgram()

    @property
    def base_element(self):
        return PointElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])

    @property
    def base_drawable(self):
        return PointGL(self.base_element)
