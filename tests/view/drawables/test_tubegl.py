#!/usr/bin/env python

import pytest

from blastsight.model.elements.tubeelement import TubeElement
from blastsight.view.integrableviewer import IntegrableViewer
from blastsight.view.drawables.tubegl import TubeGL
from blastsight.view.glprograms.tubeprogram import TubeProgram


class TestTubeGL:
    element = TubeElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], color=[1.0, 0.0, 0.0])
    element.id = 0

    def test_empty_tube(self):
        with pytest.raises(Exception):
            TubeGL()

    def test_tube_base(self):
        drawable = TubeGL(self.element)

        assert drawable
        assert drawable.id == 0

        assert not drawable.is_initialized

    def test_tube_initialize(self):
        drawable = TubeGL(self.element)
        assert not drawable.is_initialized

        drawable.initialize()

        assert drawable.is_initialized

    def test_draw(self):
        widget = IntegrableViewer()
        program = TubeProgram(widget)
        program.setup()
        program.bind()

        drawable = TubeGL(self.element)
        drawable.setup_attributes()

        program.set_drawables([drawable])
        program.draw()

        drawable.hide()
        assert not drawable.is_visible
        drawable.draw()

        drawable.show()
        assert drawable.is_visible
        drawable.draw()

        drawable.hide()
        assert not drawable.is_visible

    def test_program(self):
        widget = IntegrableViewer()
        program = TubeProgram(widget)
        program.setup()
        program.bind()

        drawable = TubeGL(self.element)
        program.set_drawables([drawable])
        program.draw()
