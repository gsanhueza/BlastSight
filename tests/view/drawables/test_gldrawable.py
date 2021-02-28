#!/usr/bin/env python

import pytest

from blastsight.model.elements.element import Element
from blastsight.view.drawables.gldrawable import GLDrawable


class TestGLDrawable:
    @pytest.fixture()
    def drawable(self):
        return GLDrawable(Element(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], id=0))

    def test_element_subset(self, drawable):
        assert all(map(lambda x: x in dir(drawable), dir(drawable.element)))
        assert not all(map(lambda x: x in dir(drawable.element), dir(drawable)))

    def test_base(self, drawable):
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

    def test_visibility(self, drawable):
        drawable.initialize()

        drawable.hide()
        assert not drawable.is_visible

        drawable.show()
        assert drawable.is_visible

        drawable.toggle_visibility()
        assert not drawable.is_visible

        drawable.toggle_visibility()
        assert drawable.is_visible

        # Not possible to test (because OpenGL), but at least it shouldn't explode
        drawable.draw()

    def test_drawable_id(self, drawable):
        assert drawable.id == 0
        drawable.id = 50
        assert drawable.id == 50
