#!/usr/bin/env python

import pytest

from minevis.view.gui.integrableviewer import IntegrableViewer
from minevis.view.drawables.axisgl import AxisGL
from minevis.view.drawables.glprograms.axisprogram import AxisProgram


class TestAxisGL:
    def test_empty_axis(self):
        with pytest.raises(Exception):
            AxisGL()

    def test_draw(self):
        widget = IntegrableViewer()
        program = AxisProgram(widget)
        program.setup()
        program.bind()

        drawable = AxisGL(type('NullElement', (), {}))
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

        drawable = AxisGL(type('NullElement', (), {}))
        program.set_drawables([drawable])
        program.draw()
