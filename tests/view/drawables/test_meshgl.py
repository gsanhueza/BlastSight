#!/usr/bin/env python

import pytest

from blastsight.model.elements.meshelement import MeshElement
from blastsight.view.drawables.meshgl import MeshGL


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

    def test_meshgl_highlighting(self):
        drawable = MeshGL(self.element)

        # The state should change regardless of initialization

        def auto_test():
            assert not drawable.is_highlighted
            drawable.toggle_highlighting()
            assert drawable.is_highlighted
            drawable.toggle_highlighting()
            assert not drawable.is_highlighted

            drawable.disable_highlighting()
            assert not drawable.is_highlighted

            drawable.enable_highlighting()
            assert drawable.is_highlighted

            drawable.disable_highlighting()
            assert not drawable.is_highlighted

        # The state should change regardless of initialization
        drawable.is_initialized = False
        auto_test()

        drawable.is_initialized = True
        auto_test()

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

    def test_mesh_program(self):
        element = MeshElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]], alpha=0.8)

        drawable_normal = MeshGL(self.element)
        drawable_alpha = MeshGL(element)
        drawable_wireframe = MeshGL(self.element, wireframe=True)
        drawable_highlight = MeshGL(self.element, highlight=True)
        drawable_highlight_alpha = MeshGL(element, highlight=True)

        assert not drawable_highlight.toggle_highlighting()
        assert drawable_highlight.toggle_highlighting()

    def test_wire_program(self):
        element = MeshElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]], alpha=0.8)

        drawable_normal = MeshGL(self.element)
        drawable_alpha = MeshGL(element)
        drawable_wireframe = MeshGL(self.element, wireframe=True)
        drawable_highlight = MeshGL(self.element, highlight=True)

        assert not drawable_highlight.toggle_highlighting()
        assert drawable_highlight.toggle_highlighting()

    def test_turbo_program(self):
        element = MeshElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]], alpha=0.8)

        drawable_normal = MeshGL(self.element, turbo=True)
        drawable_alpha = MeshGL(element, turbo=False)

        assert drawable_normal.is_boostable
        assert not drawable_alpha.is_boostable

        assert drawable_normal.is_turbo_ready
        assert not drawable_alpha.is_turbo_ready
