#!/usr/bin/env python

from blastsight.view.glprograms.wireprogram import WireProgram
from tests.view.glprograms.test_meshprogram import TestMeshProgram


class TestWireProgram(TestMeshProgram):
    @property
    def base_program(self):
        return WireProgram()
