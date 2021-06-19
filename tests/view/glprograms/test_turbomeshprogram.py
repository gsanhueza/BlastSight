#!/usr/bin/env python

from blastsight.view.drawables.meshgl import MeshGL
from blastsight.view.glprograms.turbomeshprogram import TurboMeshProgram
from tests.view.glprograms.test_meshprogram import TestMeshProgram


class TestTurboMeshProgram(TestMeshProgram):
    @property
    def base_program(self):
        return TurboMeshProgram()

    @property
    def base_drawable(self):
        return MeshGL(self.base_element, turbo=True)
