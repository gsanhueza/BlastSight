#!/usr/bin/env python

import pytest

from blastsight.model.elements.lineelement import LineElement
from blastsight.view.drawables.linegl import LineGL
from blastsight.view.glprograms.lineprogram import LineProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestLineProgram(TestShaderProgram):
    # element = LineElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0])
    # drawable = LineGL(element)

    @pytest.fixture()
    def program(self):
        return self.initialize_program(LineProgram())
