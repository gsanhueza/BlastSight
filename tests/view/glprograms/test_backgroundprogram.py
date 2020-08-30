#!/usr/bin/env python

import pytest

from blastsight.model.elements.nullelement import NullElement
from blastsight.view.drawables.backgroundgl import BackgroundGL
from blastsight.view.glprograms.backgroundprogram import BackgroundProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestBackgroundProgram(TestShaderProgram):
    element = NullElement()
    drawable = BackgroundGL(element)

    @pytest.fixture()
    def program(self):
        return self.initialize_program(BackgroundProgram())
