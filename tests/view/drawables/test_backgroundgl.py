#!/usr/bin/env python

import pytest

from caseron.view.gui.integrableviewer import IntegrableViewer
from caseron.view.drawables.backgroundgl import BackgroundGL
from caseron.view.drawables.glprograms.backgroundprogram import BackgroundProgram

from caseron.model.elements.nullelement import NullElement


class TestBackgroundGL:
    def test_empty_bg(self):
        with pytest.raises(Exception):
            BackgroundGL()

    def test_draw(self):
        widget = IntegrableViewer()
        program = BackgroundProgram(widget)
        program.setup()
        program.bind()

        drawable = BackgroundGL(NullElement())

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
        program = BackgroundProgram(widget)
        program.setup()
        program.bind()

        assert not program.color_set

        drawable = BackgroundGL(NullElement())
        program.set_drawables([drawable])
        program.draw()

        assert program.color_set
        program.draw()

        assert program.color_set
