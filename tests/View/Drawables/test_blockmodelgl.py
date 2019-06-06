#!/usr/bin/env python

import sys
import pytest

from qtpy.QtGui import QMatrix4x4
from qtpy.QtWidgets import QApplication

from Model.Elements.blockmodelelement import BlockModelElement
from View.GUI.openglwidget import OpenGLWidget
from View.Drawables.blockmodelgl import BlockModelGL


class TestBlockModelGL:
    qt_app = QApplication(sys.argv)

    element = BlockModelElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])
    element.id = 0

    def test_empty_block_model(self):
        with pytest.raises(Exception):
            BlockModelGL()

    def test_block_model_no_widget(self):
        with pytest.raises(Exception):
            BlockModelGL(widget=None, element=self.element)

    def test_block_model_base(self):
        drawable = BlockModelGL(widget=OpenGLWidget(), element=self.element)

        assert drawable
        assert drawable.id == 0
        assert isinstance(drawable.widget, OpenGLWidget)

        assert not drawable.is_initialized

    def test_block_model_initialize(self):
        drawable = BlockModelGL(widget=OpenGLWidget(), element=self.element)
        assert not drawable.is_initialized

        drawable.initialize()

        assert drawable.is_initialized

    def test_draw(self):
        drawable = BlockModelGL(widget=OpenGLWidget(), element=self.element)
        drawable.initialize()

        drawable.hide()
        assert not drawable.is_visible
        drawable.draw(None, None, None)

        drawable.show()
        assert drawable.is_visible
        drawable.draw(QMatrix4x4(), QMatrix4x4(), QMatrix4x4())

        drawable.hide()
        assert not drawable.is_visible
