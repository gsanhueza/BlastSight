#!/usr/bin/env python

import pytest

from minevis.model.elements.pointelement import PointElement
from minevis.view.gui.integrableviewer import IntegrableViewer
from minevis.view.drawables.pointgl import PointGL
from minevis.view.drawables.glprograms.pointprogram import PointProgram


class TestPointGL:
    element = PointElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])
    element.id = 0

    def test_empty_point(self):
        with pytest.raises(Exception):
            PointGL()

    def test_point_base(self):
        drawable = PointGL(self.element)

        assert drawable
        assert drawable.id == 0

        assert not drawable.is_initialized

    def test_point_initialize(self):
        drawable = PointGL(self.element)
        assert not drawable.is_initialized

        drawable.initialize()

        assert drawable.is_initialized

    def test_draw(self):
        widget = IntegrableViewer()
        program = PointProgram(widget)
        program.setup()
        program.bind()

        drawable = PointGL(self.element)
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
        program = PointProgram(widget)
        program.setup()
        program.bind()

        drawable = PointGL(self.element)
        program.set_drawables([drawable])
        program.draw()