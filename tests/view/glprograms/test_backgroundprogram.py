#!/usr/bin/env python

from blastsight.model.elements.nullelement import NullElement
from blastsight.view.drawables.backgroundgl import BackgroundGL
from blastsight.view.glprograms.backgroundprogram import BackgroundProgram
from tests.view.glprograms.test_shaderprogram import TestShaderProgram


class TestBackgroundProgram(TestShaderProgram):
    @property
    def base_program(self):
        return BackgroundProgram()

    @property
    def base_drawable(self):
        element = NullElement()
        drawable = BackgroundGL(element)

        return drawable
