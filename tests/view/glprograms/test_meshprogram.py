#!/usr/bin/env python

import pytest

from blastsight.model.elements.meshelement import MeshElement
from blastsight.view.drawables.meshgl import MeshGL
from blastsight.view.glprograms.meshprogram import MeshProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestMeshProgram(TestShaderProgram):
    # element = MeshElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[0, 1, 2])
    # drawable = MeshGL(element)

    @pytest.fixture()
    def program(self):
        return self.initialize_program(MeshProgram())
