#!/usr/bin/env python

import pytest

from caseron.view.gui.integrableviewer import IntegrableViewer
from caseron.view.drawables.axisgl import AxisGL
from caseron.view.drawables.glprograms.axisprogram import AxisProgram

from caseron.model.elements.nullelement import NullElement


class TestAxisGL:
    def test_empty_axis(self):
        with pytest.raises(Exception):
            AxisGL()

    def test_draw(self):
        widget = IntegrableViewer()
        program = AxisProgram(widget)
        program.setup()
        program.bind()

        drawable = AxisGL(NullElement())
        drawable.setup_attributes()

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
        program = AxisProgram(widget)
        program.setup()
        program.bind()

        drawable = AxisGL(NullElement())
        program.set_drawables([drawable])
        program.draw()
