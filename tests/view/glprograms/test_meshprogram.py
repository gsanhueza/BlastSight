#!/usr/bin/env python

from blastsight.model.elements.meshelement import MeshElement
from blastsight.view.drawables.meshgl import MeshGL
from blastsight.view.glprograms.meshprogram import MeshProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestMeshProgram(TestShaderProgram):
    @property
    def base_program(self):
        return MeshProgram()

    @property
    def base_drawable(self):
        element = MeshElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[0, 1, 2])
        drawable = MeshGL(element)

        return drawable
