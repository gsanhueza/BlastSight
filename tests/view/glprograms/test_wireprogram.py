#!/usr/bin/env python

from blastsight.view.drawables.meshgl import MeshGL
from blastsight.view.glprograms.wireprogram import WireProgram
from tests.view.glprograms.test_meshprogram import TestMeshProgram


class TestWireProgram(TestMeshProgram):
    @property
    def base_program(self):
        return WireProgram()

    @property
    def base_drawable(self):
        return MeshGL(self.base_element, wireframe=True)
