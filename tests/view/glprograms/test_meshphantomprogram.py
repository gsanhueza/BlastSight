#!/usr/bin/env python

import pytest

from blastsight.view.glprograms.meshphantomprogram import MeshPhantomProgram
from tests.view.glprograms.test_meshprogram import TestMeshProgram


class TestMeshPhantomProgram(TestMeshProgram):
    @pytest.fixture()
    def program(self):
        return self.initialize_program(MeshPhantomProgram())
