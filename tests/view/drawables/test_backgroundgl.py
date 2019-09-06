#!/usr/bin/env python

import pytest

from minevis.view.gui.integrableviewer import IntegrableViewer
from minevis.view.drawables.backgroundgl import BackgroundGL
from minevis.view.drawables.glprograms.backgroundprogram import BackgroundProgram


class TestBackgroundGL:
    def test_empty_line(self):
        with pytest.raises(Exception):
            BackgroundGL()

    def test_line_no_widget(self):
        with pytest.raises(Exception):
            BackgroundGL(widget=None, element=type('NullElement', (), {}))

    def test_draw(self):
        widget = IntegrableViewer()
        program = BackgroundProgram(widget)
        program.setup()
        program.bind()

        drawable = BackgroundGL(widget=IntegrableViewer(), element=type('NullElement', (), {}))

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

        drawable = BackgroundGL(widget=IntegrableViewer(), element=type('NullElement', (), {}))
        program.set_drawables([drawable])
        program.draw()

        assert program.color_set
        program.draw()

        assert program.color_set
