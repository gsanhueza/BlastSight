#!/usr/bin/env python

import pytest

from blastsight.model.elements.tubeelement import TubeElement
from blastsight.view.drawables.tubegl import TubeGL
from blastsight.view.glprograms.tubeprogram import TubeProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestTubeProgram(TestShaderProgram):
    element = TubeElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0])
    drawable = TubeGL(element)

    @pytest.fixture()
    def program(self):
        return self.initialize_program(TubeProgram())
