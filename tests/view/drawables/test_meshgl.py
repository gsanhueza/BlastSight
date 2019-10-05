#!/usr/bin/env python

import pytest

from blastsight.model.elements.meshelement import MeshElement
from blastsight.view.integrableviewer import IntegrableViewer
from blastsight.view.drawables.meshgl import MeshGL
from blastsight.view.drawables.glprograms.meshprogram import MeshProgram
from blastsight.view.drawables.glprograms.wireprogram import WireProgram


class TestMeshGL:
    element = MeshElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])
    element.id = 0

    def test_empty_mesh(self):
        with pytest.raises(Exception):
            MeshGL()

    def test_meshgl_base(self):
        drawable = MeshGL(self.element)

        assert drawable
        assert drawable.id == 0

        assert not drawable.is_initialized

    def test_meshgl_initialize(self):
        drawable = MeshGL(self.element)
        assert not drawable.is_initialized

        drawable.initialize()

        assert drawable.is_initialized

    def test_meshgl_wireframe_no_init(self):
        drawable = MeshGL(self.element)

        assert not drawable.is_wireframed
        drawable.toggle_wireframe()
        assert drawable.is_wireframed
        drawable.toggle_wireframe()
        assert not drawable.is_wireframed

    def test_meshgl_wireframe(self):
        drawable = MeshGL(self.element)
        # The state should change regardless of initialization

        def auto_test():
            assert not drawable.is_wireframed
            drawable.toggle_wireframe()
            assert drawable.is_wireframed
            drawable.toggle_wireframe()
            assert not drawable.is_wireframed

            drawable.disable_wireframe()
            assert not drawable.is_wireframed

            drawable.enable_wireframe()
            assert drawable.is_wireframed

            drawable.disable_wireframe()
            assert not drawable.is_wireframed

        # The state should change regardless of initialization
        drawable.is_initialized = False
        auto_test()

        drawable.is_initialized = True
        auto_test()

    def test_draw(self):
        widget = IntegrableViewer()
        program = MeshProgram(widget)
        program.setup()
        program.bind()

        drawable = MeshGL(self.element)
        drawable.setup_attributes()

        program.set_drawables([drawable])
        program.draw()

        drawable.hide()
        assert not drawable.is_visible
        drawable.draw()

        drawable.show()
        assert drawable.is_visible
        drawable.draw()

        drawable.hide()
        assert not drawable.is_visible

    def test_program(self):
        widget = IntegrableViewer()
        program = MeshProgram(widget)
        element = MeshElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]], alpha=0.8)
        program.setup()
        program.bind()

        drawable_normal = MeshGL(self.element)
        drawable_alpha = MeshGL(element)
        drawable_wireframe = MeshGL(self.element, wireframe=True)
        drawable_highlight = MeshGL(self.element, highlight=True)

        assert not drawable_highlight.toggle_highlighting()
        assert drawable_highlight.toggle_highlighting()

        program.set_drawables([drawable_normal,
                               drawable_alpha,
                               drawable_wireframe,
                               drawable_highlight])
        program.draw()

    def test_wire_program(self):
        widget = IntegrableViewer()
        program = WireProgram(widget)
        element = MeshElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]], alpha=0.8)
        program.setup()
        program.bind()

        drawable_normal = MeshGL(self.element)
        drawable_alpha = MeshGL(element)
        drawable_wireframe = MeshGL(self.element, wireframe=True)
        drawable_highlight = MeshGL(self.element, highlight=True)

        assert not drawable_highlight.toggle_highlighting()
        assert drawable_highlight.toggle_highlighting()

        program.set_drawables([drawable_normal,
                               drawable_alpha,
                               drawable_wireframe,
                               drawable_highlight])
        program.draw()
