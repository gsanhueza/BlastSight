#!/usr/bin/env python

import pytest

from blastsight.view.glprograms.highlightprogram import HighlightProgram
from tests.view.glprograms.test_meshprogram import TestMeshProgram


class TestHighlightProgram(TestMeshProgram):
    @pytest.fixture()
    def program(self):
        return self.initialize_program(HighlightProgram())
