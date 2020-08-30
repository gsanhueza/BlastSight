#!/usr/bin/env python

import pytest

from blastsight.view.glprograms.meshprogram import MeshProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestMeshProgram(TestShaderProgram):
    @pytest.fixture()
    def program(self):
        return self.initialize_program(MeshProgram())
