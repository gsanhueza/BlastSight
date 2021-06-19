#!/usr/bin/env python

from blastsight.view.glprograms.xsectionmeshprogram import XSectionMeshProgram
from tests.view.glprograms.test_meshprogram import TestMeshProgram


class TestXSectionMeshProgram(TestMeshProgram):
    @property
    def base_program(self):
        return XSectionMeshProgram()
