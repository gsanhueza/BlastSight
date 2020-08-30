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
        return self.initialize_program(AxisProgram())

    def test_draw(self, program):
        # If the uniform hasn't been updated, we still do not have the value
        with pytest.raises(Exception):
            super().test_draw(program)

        program.update_uniform('viewport', 1280, 720)
        super().test_draw(program)
