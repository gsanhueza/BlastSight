#!/usr/bin/env python

import pytest

from libraries.Model.Elements.blockelement import BlockElement
from libraries.View.GUI.integrableviewer import IntegrableViewer
from libraries.View.Drawables.blockgl import BlockGL
from libraries.View.Drawables.blockprogram import BlockProgram


class TestBlockModelGL:
    element = BlockElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])
    element.id = 0

    def test_empty_block_model(self):
        with pytest.raises(Exception):
            BlockGL()

    def test_block_model_no_widget(self):
        with pytest.raises(Exception):
            BlockGL(widget=None, element=self.element)

    def test_block_model_base(self):
        drawable = BlockGL(widget=IntegrableViewer(), element=self.element)

        assert drawable
        assert drawable.id == 0
        assert isinstance(drawable.widget, IntegrableViewer)

        assert not drawable.is_initialized

    def test_block_model_initialize(self):
        drawable = BlockGL(widget=IntegrableViewer(), element=self.element)
        assert not drawable.is_initialized

        drawable.initialize()

        assert drawable.is_initialized

    def test_draw(self):
        widget = IntegrableViewer()
        program = BlockProgram(widget)
        program.setup()
        program.bind()

        drawable = BlockGL(widget=IntegrableViewer(), element=self.element)
        drawable.setup_attributes()

        drawable.hide()
        assert not drawable.is_visible
        drawable.draw()

        drawable.show()
        assert drawable.is_visible
        drawable.draw()

        drawable.hide()
        assert not drawable.is_visible
