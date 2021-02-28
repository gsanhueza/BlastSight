#!/usr/bin/env python

import pytest

from blastsight.model.elements.nullelement import NullElement
from blastsight.view.drawables.gridgl import GridGL
from blastsight.view.glprograms.gridprogram import GridProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestGridProgram(TestShaderProgram):
    # element = NullElement()
    # drawable = GridGL(element)

    @pytest.fixture()
    def program(self):
        return self.initialize_program(GridProgram())
