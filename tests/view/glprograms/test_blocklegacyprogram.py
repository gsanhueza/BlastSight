#!/usr/bin/env python

import pytest

from blastsight.model.elements.blockelement import BlockElement
from blastsight.view.drawables.blockgl import BlockGL
from blastsight.view.glprograms.blocklegacyprogram import BlockLegacyProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestBlockLegacyProgram(TestShaderProgram):
    element = BlockElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])
    drawable = BlockGL(element, legacy=True)

    @pytest.fixture()
    def program(self):
        return self.initialize_program(BlockLegacyProgram())
