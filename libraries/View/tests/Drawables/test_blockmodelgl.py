#!/usr/bin/env python

import pytest

from qtpy.QtGui import QMatrix4x4

from libraries.Model.Elements.blockmodelelement import BlockModelElement
from libraries.View.GUI.integrableviewer import IntegrableViewer
from libraries.View.Drawables.blockmodelgl import BlockModelGL


class TestBlockModelGL:
    element = BlockModelElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])
    element.id = 0

    def test_empty_block_model(self):
        with pytest.raises(Exception):
            BlockModelGL()

    def test_block_model_no_widget(self):
        with pytest.raises(Exception):
            BlockModelGL(widget=None, element=self.element)

    def test_block_model_base(self):
        drawable = BlockModelGL(widget=IntegrableViewer(), element=self.element)

        assert drawable
        assert drawable.id == 0
        assert isinstance(drawable.widget, IntegrableViewer)

        assert not drawable.is_initialized

    def test_block_model_initialize(self):
        drawable = BlockModelGL(widget=IntegrableViewer(), element=self.element)
        assert not drawable.is_initialized

        drawable.initialize()

        assert drawable.is_initialized

    def test_draw(self):
        drawable = BlockModelGL(widget=IntegrableViewer(), element=self.element)
        drawable.initialize()

        drawable.hide()
        assert not drawable.is_visible
        drawable.draw()

        drawable.show()
        assert drawable.is_visible
        drawable.draw()

        drawable.hide()
        assert not drawable.is_visible
