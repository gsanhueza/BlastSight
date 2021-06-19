#!/usr/bin/env python

import pytest

from blastsight.model.elements.nullelement import NullElement
from blastsight.view.glprograms.shaderprogram import ShaderProgram
from blastsight.view.drawables import GLDrawable


class TestShaderProgram:
    @property
    def base_program(self):
        return ShaderProgram()

    @property
    def base_element(self):
        return NullElement()

    @property
    def base_drawable(self):
        return GLDrawable(self.base_element)

    def generate_program(self):
        prog = self.base_program
        prog.set_drawables([self.base_drawable])

        return prog

    @staticmethod
    def initialize_program(_program, _drawable):
        assert _program.shader_program is None

        _program.set_drawables([_drawable])
        _program.initialize()

        assert _program.shader_program is not None

        return _program

    @pytest.fixture()
    def program(self):
        return self.generate_program()

    def test_program(self, program):
        assert program.shader_program is None

        program.initialize()

        assert program.shader_program is not None

    def test_draw(self, program):
        assert len(program.opaques) == 1
        assert len(program.transparents) == 0

        program.draw()
        program.redraw()
