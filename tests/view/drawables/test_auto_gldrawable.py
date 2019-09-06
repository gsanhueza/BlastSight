#!/usr/bin/env python

import sys

from qtpy.QtWidgets import QApplication

from minevis.model.elements.element import Element
from minevis.view.drawables.gldrawable import GLDrawable
from minevis.view.gui.integrableviewer import IntegrableViewer
from minevis.view.drawables.glprograms.shaderprogram import ShaderProgram


class TestBaseDrawables:
    qt_app = QApplication(sys.argv)

    # Needed to create OpenGLWidget.context()
    widget = IntegrableViewer()
    widget.show()
    widget.hide()

    element = Element(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0])
    element.id = 0

    def test_base(self):
        assert GLDrawable(widget=self.widget, element=self.element)

    def test_drawable_id(self):
        drawable = GLDrawable(widget=self.widget, element=self.element)
        assert drawable.id == self.element.id

        drawable.id = 50
        assert drawable.id == 50

    def test_program(self):
        widget = IntegrableViewer()
        program = ShaderProgram(widget)
        program.setup()
        program.bind()
        program.setup()  # Deliberately duplicated

        drawable = GLDrawable(widget=self.widget, element=self.element)
        program.set_drawables([drawable])
        program.draw()

    def test_cleanup(self):
        drawable = GLDrawable(widget=self.widget, element=self.element)
        drawable.cleanup()
        drawable.initialize()
        drawable.cleanup()

    def test_draw(self):
        widget = IntegrableViewer()
        program = ShaderProgram(widget)
        program.setup()
        program.bind()

        drawable = GLDrawable(widget=self.widget, element=self.element)
        drawable.setup_attributes()

        program.set_drawables([drawable])
        program.draw()

        # Standard
        drawable.hide()
        assert not drawable.is_visible
        drawable.draw()

        drawable.show()
        assert drawable.is_visible
        drawable.draw()

        drawable.hide()
        assert not drawable.is_visible

        # Toggle
        drawable.show()
        assert drawable.is_visible

        drawable.toggle_visibility()
        assert not drawable.is_visible

        drawable.toggle_visibility()
        assert drawable.is_visible
