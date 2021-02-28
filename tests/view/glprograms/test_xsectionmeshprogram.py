#!/usr/bin/env python

import pytest

from blastsight.view.glprograms.xsectionmeshprogram import XSectionMeshProgram
from tests.view.glprograms.test_meshprogram import TestMeshProgram


class TestXSectionMeshProgram(TestMeshProgram):
    @pytest.fixture()
    def program(self):
        return self.initialize_program(XSectionMeshProgram())
