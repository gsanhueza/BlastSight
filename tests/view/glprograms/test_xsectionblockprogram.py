#!/usr/bin/env python

from blastsight.view.glprograms.xsectionblockprogram import XSectionBlockProgram
from tests.view.glprograms.test_blockprogram import TestBlockProgram


class TestXSectionBlockProgram(TestBlockProgram):
    @property
    def base_program(self):
        return XSectionBlockProgram()
