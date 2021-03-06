#!/usr/bin/env python

import pytest

from blastsight.model.elements.pointelement import PointElement
from blastsight.view.drawables.pointgl import PointGL
from blastsight.view.glprograms.pointprogram import PointProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestPointProgram(TestShaderProgram):
    element = PointElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])
    drawable = PointGL(element)

    @pytest.fixture()
    def program(self):
        return self.initialize_program(PointProgram())
