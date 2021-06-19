#!/usr/bin/env python

import pytest

from blastsight.model.elements.meshelement import MeshElement
from blastsight.view.drawables.meshgl import MeshGL
from tests.view.drawables.test_gldrawable import TestGLDrawable


class TestMeshGL(TestGLDrawable):
    @pytest.fixture()
    def drawable(self):
        return MeshGL(MeshElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]], id=0))

    def test_empty_mesh(self):
        with pytest.raises(Exception):
            MeshGL()

    def test_highlight(self, drawable):
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

    def test_wireframe(self, drawable):
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
