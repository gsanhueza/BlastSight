#!/usr/bin/env python

import sys

from PyQt5.QtWidgets import QApplication

from Model.Elements.element import Element
from View.Drawables.gldrawable import GLDrawable
from View.GUI.openglwidget import OpenGLWidget


class TestGLDrawable:
    qt_app = QApplication(sys.argv)

    # FIXME Why do we need to run this before to avoid a segfault, even if we don't use it anywhere?
    # Needed to create OpenGLWidget.context()
    widget = OpenGLWidget()
    widget.show()
    widget.hide()

    element = Element(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0])
    element.id = 0

    def test_base(self):
        assert GLDrawable(widget=OpenGLWidget(), element=self.element)

    def test_drawable_id(self):
        drawable = GLDrawable(widget=OpenGLWidget(), element=self.element)
        assert drawable.id == self.element.id

        drawable.id = 50
        assert drawable.id == 50
