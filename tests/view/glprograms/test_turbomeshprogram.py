#!/usr/bin/env python

from blastsight.model.elements.meshelement import MeshElement
from blastsight.view.drawables.meshgl import MeshGL
from blastsight.view.glprograms.turbomeshprogram import TurboMeshProgram
from tests.view.glprograms.test_meshprogram import TestMeshProgram


class TestTurboMeshProgram(TestMeshProgram):
    @property
    def base_program(self):
        return TurboMeshProgram()

    @property
    def base_drawable(self):
        element = MeshElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[0, 1, 2])
        drawable = MeshGL(element, turbo=True)

        return drawable
