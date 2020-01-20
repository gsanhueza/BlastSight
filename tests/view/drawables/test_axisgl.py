#!/usr/bin/env python

from blastsight.view.integrableviewer import IntegrableViewer
from blastsight.view.drawables.axisgl import AxisGL
from blastsight.view.glprograms.axisprogram import AxisProgram

from blastsight.model.elements.nullelement import NullElement


class TestAxisGL:
    def test_empty_axis(self):
        drawable = AxisGL()
        assert type(drawable.element) is NullElement

    def test_dir(self):
        assert len(dir(AxisGL())) > 0

    def test_draw(self):
        viewer = IntegrableViewer()
        program = AxisProgram(viewer)
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
        viewer = IntegrableViewer()
        program = AxisProgram(viewer)
        program.setup()
        program.bind()

        drawable = AxisGL(NullElement())
        program.set_drawables([drawable])
        program.draw()
