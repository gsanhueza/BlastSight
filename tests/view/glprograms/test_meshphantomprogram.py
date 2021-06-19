#!/usr/bin/env python

from blastsight.view.glprograms.meshphantomprogram import MeshPhantomProgram
from tests.view.glprograms.test_meshprogram import TestMeshProgram


class TestMeshPhantomProgram(TestMeshProgram):
    @property
    def base_program(self):
        return MeshPhantomProgram()
