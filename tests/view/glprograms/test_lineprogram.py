#!/usr/bin/env python

import pytest

from blastsight.view.glprograms.lineprogram import LineProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestLineProgram(TestShaderProgram):
    @pytest.fixture()
    def program(self):
        return self.initialize_program(LineProgram())
