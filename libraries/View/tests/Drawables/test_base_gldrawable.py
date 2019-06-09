#!/usr/bin/env python

import sys

from qtpy.QtWidgets import QApplication

from libraries.Model.Elements.element import Element
from libraries.View.Drawables.gldrawable import GLDrawable
from libraries.View.GUI.integrableviewer import IntegrableViewer


class TestBaseDrawables:
    qt_app = QApplication(sys.argv)

    # Needed to create OpenGLWidget.context()
    widget = IntegrableViewer()
    widget.show()
    widget.hide()

    element = Element(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0])
    element.id = 0

    def test_base(self):
        assert GLDrawable(widget=IntegrableViewer(), element=self.element)

    def test_drawable_id(self):
        drawable = GLDrawable(widget=IntegrableViewer(), element=self.element)
        assert drawable.id == self.element.id

        drawable.id = 50
        assert drawable.id == 50
