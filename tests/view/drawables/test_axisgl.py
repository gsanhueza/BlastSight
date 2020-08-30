#!/usr/bin/env python

from blastsight.view.integrableviewer import IntegrableViewer
from blastsight.view.drawables.axisgl import AxisGL
from blastsight.view.glprograms.axisprogram import AxisProgram

from blastsight.model.elements.nullelement import NullElement


class TestAxisGL:
    def test_dir(self):
        assert len(dir(AxisGL())) > 0

    def test_draw(self):
        program = AxisProgram()
        program.initialize()
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
