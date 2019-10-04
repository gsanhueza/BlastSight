#!/usr/bin/env python

import sys

from qtpy.QtWidgets import QApplication

from caseron.model.elements.element import Element
from caseron.view.drawables.gldrawable import GLDrawable
from caseron.view.integrableviewer import IntegrableViewer
from caseron.view.drawables.glprograms.shaderprogram import ShaderProgram


class TestAutoDrawable:
    qt_app = QApplication(sys.argv)

    # Needed to create OpenGLWidget.context()
    widget = IntegrableViewer()
    widget.show()
    widget.hide()

    element = Element(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0])
    element.id = 0

    def test_base(self):
        drawable = GLDrawable(self.element)
        assert drawable

        # This is a hack in GLDrawable.
        # Check its source code to understand what and why we're testing this.
        assert len(dir(drawable)) >= len(dir(self.element))
        for dir_e in dir(self.element):
            assert dir_e in dir(drawable)

    def test_drawable_id(self):
        drawable = GLDrawable(self.element)
        assert drawable.id == self.element.id

        drawable.id = 50
        assert drawable.id == 50

    def test_program(self):
        widget = IntegrableViewer()
        program = ShaderProgram(widget)
        program.setup()
        program.bind()
        program.setup()  # Deliberately duplicated

        drawable = GLDrawable(self.element)
        program.set_drawables([drawable])
        program.draw()

    def test_cleanup(self):
        drawable = GLDrawable(self.element)
        drawable.cleanup()
        drawable.initialize()
        drawable.cleanup()

    def test_draw(self):
        widget = IntegrableViewer()
        program = ShaderProgram(widget)
        program.setup()
        program.bind()

        drawable = GLDrawable(self.element)
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
