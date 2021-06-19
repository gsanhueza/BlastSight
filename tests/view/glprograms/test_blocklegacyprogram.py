#!/usr/bin/env python

from blastsight.model.elements.blockelement import BlockElement
from blastsight.view.drawables.blockgl import BlockGL
from blastsight.view.glprograms.blocklegacyprogram import BlockLegacyProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestBlockLegacyProgram(TestShaderProgram):
    @property
    def base_program(self):
        return BlockLegacyProgram()

    @property
    def base_element(self):
        return BlockElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])

    @property
    def base_drawable(self):
        return BlockGL(self.base_element, legacy=True)
