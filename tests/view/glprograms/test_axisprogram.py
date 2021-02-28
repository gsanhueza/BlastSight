#!/usr/bin/env python

import pytest

from blastsight.model.elements.nullelement import NullElement
from blastsight.view.drawables.axisgl import AxisGL
from blastsight.view.glprograms.gridprogram import GridProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestAxisProgram(TestShaderProgram):
    element = NullElement()
    drawable = AxisGL(element)

    @pytest.fixture()
    def program(self):
        return self.initialize_program(GridProgram())
