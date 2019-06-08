#!/usr/bin/env python

import pytest

from qtpy.QtGui import QMatrix4x4

from libraries.Model.Elements.lineelement import LineElement
from libraries.View.GUI.openglwidget import OpenGLWidget
from libraries.View.Drawables.linegl import LineGL


class TestLineGL:
    element = LineElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], color=[1.0, 0.0, 0.0])
    element.id = 0

    def test_empty_line(self):
        with pytest.raises(Exception):
            LineGL()

    def test_line_no_widget(self):
        with pytest.raises(Exception):
            LineGL(widget=None, element=self.element)

    def test_line_base(self):
        drawable = LineGL(widget=OpenGLWidget(), element=self.element)

        assert drawable
        assert drawable.id == 0
        assert isinstance(drawable.widget, OpenGLWidget)

        assert not drawable.is_initialized

    def test_line_initialize(self):
        drawable = LineGL(widget=OpenGLWidget(), element=self.element)
        assert not drawable.is_initialized

        drawable.initialize()

        assert drawable.is_initialized

    def test_draw(self):
        drawable = LineGL(widget=OpenGLWidget(), element=self.element)
        drawable.initialize()

        drawable.hide()
        assert not drawable.is_visible
        drawable.draw(None, None, None)

        drawable.show()
        assert drawable.is_visible
        drawable.draw(QMatrix4x4(), QMatrix4x4(), QMatrix4x4())

        drawable.hide()
        assert not drawable.is_visible
