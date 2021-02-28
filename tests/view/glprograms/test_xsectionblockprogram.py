#!/usr/bin/env python

import pytest

from blastsight.model.elements.blockelement import BlockElement
from blastsight.view.drawables.blockgl import BlockGL
from blastsight.view.glprograms.xsectionblockprogram import XSectionBlockProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestXSectionBlockProgram(TestShaderProgram):
    element = BlockElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])
    drawable = BlockGL(element)

    @pytest.fixture()
    def program(self):
        _program = self.initialize_program(XSectionBlockProgram())
        _program.uniform_values['block_size'] = [15.0, 15.0, 10.0]
        return _program
