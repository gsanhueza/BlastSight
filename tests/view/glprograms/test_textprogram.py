#!/usr/bin/env python

import pytest

from blastsight.model.elements.nullelement import NullElement
from blastsight.view.drawables.textgl import TextGL
from blastsight.view.glprograms.textprogram import TextProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestTextProgram(TestShaderProgram):
    element = NullElement()
    drawable = TextGL(element)

    @pytest.fixture()
    def program(self):
        return self.initialize_program(TextProgram())
