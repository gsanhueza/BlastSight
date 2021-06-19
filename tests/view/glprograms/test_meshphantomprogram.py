#!/usr/bin/env python

from blastsight.view.drawables.meshgl import MeshGL
from blastsight.view.glprograms.meshphantomprogram import MeshPhantomProgram
from tests.view.glprograms.test_meshprogram import TestMeshProgram


class TestMeshPhantomProgram(TestMeshProgram):
    @property
    def base_program(self):
        return MeshPhantomProgram()

    @property
    def base_drawable(self):
        return MeshGL(self.base_element, phantom=True)
