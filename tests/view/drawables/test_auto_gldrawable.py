#!/usr/bin/env python

import sys

from qtpy.QtWidgets import QApplication

from blastsight.model.elements.element import Element
from blastsight.view.drawables.gldrawable import GLDrawable
from blastsight.view.integrableviewer import IntegrableViewer
from blastsight.view.glprograms.shaderprogram import ShaderProgram


class TestAutoDrawable:
    qt_app = QApplication(sys.argv)

    # Needed to create OpenGLWidget.context()
    viewer = IntegrableViewer()
    viewer.show()
    viewer.hide()

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

    def test_program(self):
        viewer = IntegrableViewer()
        program = ShaderProgram(viewer)
        program.setup()
        program.bind()

        drawable = GLDrawable(self.element)
        program.set_drawables([drawable])
        program.draw()

    def test_cleanup(self):
        drawable = GLDrawable(self.element)
        assert len(drawable.vaos) == 0
        drawable.initialize()
        drawable.cleanup()
        assert len(drawable.vaos) == 0

    def test_draw(self):
        viewer = IntegrableViewer()
        program = ShaderProgram(viewer)
        assert program.shader_program is None
        program.setup()
        assert program.shader_program is not None
        program_id = id(program.shader_program)
        program.bind()

        program.setup()
        assert program.shader_program is not None
        assert program_id == id(program.shader_program)

        drawable = GLDrawable(self.element)
        drawable.setup_attributes()

        program.set_drawables([drawable])
        program.draw()
        program.redraw()

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
