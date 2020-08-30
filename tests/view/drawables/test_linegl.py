#!/usr/bin/env python

import pytest

from blastsight.model.elements.lineelement import LineElement
from blastsight.view.integrableviewer import IntegrableViewer
from blastsight.view.drawables.linegl import LineGL
from blastsight.view.glprograms.lineprogram import LineProgram


class TestLineGL:
    element = LineElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], color=[1.0, 0.0, 0.0])
    element.id = 0

    def test_empty_line(self):
        with pytest.raises(Exception):
            LineGL()

    def test_line_base(self):
        drawable = LineGL(self.element)

        assert drawable
        assert drawable.id == 0

        assert not drawable.is_initialized

    def test_line_initialize(self):
        drawable = LineGL(self.element)
        assert not drawable.is_initialized

        drawable.initialize()

        assert drawable.is_initialized

    def test_draw(self):
        viewer = IntegrableViewer()
        program = LineProgram()
        program.initialize(viewer)
        program.bind()

        drawable = LineGL(self.element)
        drawable.setup_attributes()

        drawable.hide()
        assert not drawable.is_visible
        drawable.draw()

        drawable.show()
        assert drawable.is_visible
        drawable.draw()

        drawable.hide()
        assert not drawable.is_visible
