#!/usr/bin/env python

import sys

from qtpy.QtWidgets import QApplication

from blastsight.model.elements.element import Element
from blastsight.view.drawables.gldrawable import GLDrawable
from blastsight.view.integrableviewer import IntegrableViewer


class TestAutoDrawable:
    qt_app = QApplication(sys.argv)

    # Needed to create OpenGLWidget.context()
    viewer = IntegrableViewer()
    viewer.show()
    viewer.hide()

    element = Element(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0])
    element.id = 0

    @staticmethod
    def is_subset(subset, superset):
        for element in subset:
            if element not in superset:
                return False
        return True

    def test_base(self):
        drawable = GLDrawable(self.element)
        assert drawable

        # This is a hack in GLDrawable.
        # Check its source code to understand what and why we're testing this.
        assert len(dir(drawable)) >= len(dir(self.element))
        assert self.is_subset(dir(self.element), dir(drawable))

        assert not drawable.is_initialized
        assert not drawable.is_boostable
        assert drawable.is_visible

        drawable.initialize()
        drawable.is_boostable = True

        assert drawable.is_initialized
        assert drawable.is_boostable
        assert drawable.is_visible

        drawable.initialize()
        assert drawable.is_initialized

    def test_drawable_id(self):
        drawable = GLDrawable(self.element)
        assert drawable.id == self.element.id

        drawable.id = 50
        assert drawable.id == 50

    def test_cleanup(self):
        drawable = GLDrawable(self.element)
        assert len(drawable._vaos) == 0
        drawable.initialize()
        drawable.cleanup()
        assert len(drawable._vaos) == 0

