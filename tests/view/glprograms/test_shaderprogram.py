#!/usr/bin/env python

import pytest

from blastsight.model.elements.nullelement import NullElement
from blastsight.view.glprograms.shaderprogram import ShaderProgram
from blastsight.view.drawables import GLDrawable


class TestShaderProgram:
    element = NullElement()
    drawable = GLDrawable(element)

    @staticmethod
    def initialize_program(_program):
        assert _program.shader_program is None
        _program.initialize()
        assert _program.shader_program is not None
        return _program

    @pytest.fixture()
    def program(self):
        return self.initialize_program(ShaderProgram())

    def test_draw(self, program):
        program.set_drawables([self.drawable])
        assert len(program.opaques) == 1
        assert len(program.transparents) == 0

        program.draw()
        program.redraw()
