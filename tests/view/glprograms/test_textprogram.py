#!/usr/bin/env python

from blastsight.model.elements.nullelement import NullElement
from blastsight.view.drawables.textgl import TextGL
from blastsight.view.glprograms.textprogram import TextProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestTextProgram(TestShaderProgram):
    @property
    def base_program(self):
        return TextProgram()

    @property
    def base_drawable(self):
        element = NullElement()
        drawable = TextGL(element)

        return drawable
