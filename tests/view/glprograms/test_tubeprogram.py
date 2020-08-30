#!/usr/bin/env python

import pytest

from blastsight.view.glprograms.tubeprogram import TubeProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestTubeProgram(TestShaderProgram):
    @pytest.fixture()
    def program(self):
        return self.initialize_program(TubeProgram())
