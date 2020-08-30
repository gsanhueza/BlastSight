#!/usr/bin/env python

import pytest

from blastsight.view.glprograms.wireprogram import WireProgram
from tests.view.glprograms.test_meshprogram import TestMeshProgram


class TestWireProgram(TestMeshProgram):
    @pytest.fixture()
    def program(self):
        return self.initialize_program(WireProgram())
