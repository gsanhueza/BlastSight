#!/usr/bin/env python

from blastsight.model.elements.blockelement import BlockElement
from blastsight.view.drawables.blockgl import BlockGL
from blastsight.view.glprograms.xsectionblockprogram import XSectionBlockProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestXSectionBlockProgram(TestShaderProgram):
    @property
    def base_program(self):
        return XSectionBlockProgram()

    @property
    def base_drawable(self):
        element = BlockElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])
        drawable = BlockGL(element)

        return drawable

    def generate_program(self):
        prog = super().generate_program()
        prog.uniform_values['block_size'] = [15.0, 15.0, 10.0]

        return prog
