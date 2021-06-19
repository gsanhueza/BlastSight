#!/usr/bin/env python

from blastsight.view.glprograms.highlightprogram import HighlightProgram
from tests.view.glprograms.test_meshprogram import TestMeshProgram


class TestHighlightProgram(TestMeshProgram):
    @property
    def base_program(self):
        return HighlightProgram()
