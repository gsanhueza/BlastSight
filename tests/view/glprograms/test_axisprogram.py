#!/usr/bin/env python

from blastsight.model.elements.nullelement import NullElement
from blastsight.view.drawables.axisgl import AxisGL
from blastsight.view.glprograms.axisprogram import AxisProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestAxisProgram(TestShaderProgram):
    @property
    def base_program(self):
        return AxisProgram()

    @property
    def base_drawable(self):
        element = NullElement()
        drawable = AxisGL(element)

        return drawable

    def generate_program(self):
        prog = super().generate_program()
        prog.uniform_values['viewport'] = [1920, 1080]

        return prog
