#!/usr/bin/env python

import pytest

from blastsight.model.elements.nullelement import NullElement
from blastsight.view.drawables.axisgl import AxisGL
from blastsight.view.glprograms.axisprogram import AxisProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestAxisProgram(TestShaderProgram):
    element = NullElement()
    drawable = AxisGL(element)

    @pytest.fixture()
    def program(self):
        _program = self.initialize_program(AxisProgram())
        _program.uniform_values['viewport'] = [1920, 1080]
        return _program
