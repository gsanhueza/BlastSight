#!/usr/bin/env python

import pytest

from blastsight.view.integrableviewer import IntegrableViewer
from blastsight.view.drawables.axisgl import AxisGL
from blastsight.view.drawables.glprograms.axisprogram import AxisProgram

from blastsight.model.elements.nullelement import NullElement


class TestAxisGL:
    def test_empty_axis(self):
        with pytest.raises(Exception):
            AxisGL()

    def test_dir(self):
        assert len(dir(AxisGL(NullElement()))) > 0

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
