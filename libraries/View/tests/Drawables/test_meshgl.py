#!/usr/bin/env python

import pytest

from qtpy.QtGui import QMatrix4x4

from libraries.Model.Elements.meshelement import MeshElement
from libraries.View.GUI.integrableviewer import IntegrableViewer
from libraries.View.Drawables.meshgl import MeshGL


class TestMeshGL:
    element = MeshElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])
    element.id = 0

    def test_empty_meshgl(self):
        with pytest.raises(Exception):
            MeshGL()

    def test_meshgl_no_widget(self):
        with pytest.raises(Exception):
            MeshGL(widget=None, element=self.element)

    def test_meshgl_base(self):
        drawable = MeshGL(widget=IntegrableViewer(), element=self.element)

        assert drawable
        assert drawable.id == 0
        assert isinstance(drawable.widget, IntegrableViewer)

        assert not drawable.is_initialized

    def test_meshgl_initialize(self):
        drawable = MeshGL(widget=IntegrableViewer(), element=self.element)
        assert not drawable.is_initialized

        drawable.initialize()

        assert drawable.is_initialized

    def test_meshgl_wireframe_no_init(self):
        drawable = MeshGL(widget=IntegrableViewer(), element=self.element)

        assert not drawable.wireframe_enabled
        drawable.toggle_wireframe()
        assert drawable.wireframe_enabled
        drawable.toggle_wireframe()
        assert not drawable.wireframe_enabled

    def test_meshgl_wireframe(self):
        drawable = MeshGL(widget=IntegrableViewer(), element=self.element)
        drawable.initialize()

        assert not drawable.wireframe_enabled
        drawable.toggle_wireframe()
        assert drawable.wireframe_enabled
        drawable.toggle_wireframe()
        assert not drawable.wireframe_enabled

    def test_draw(self):
        drawable = MeshGL(widget=IntegrableViewer(), element=self.element)
        drawable.initialize()

        drawable.hide()
        assert not drawable.is_visible
        drawable.draw()

        drawable.show()
        assert drawable.is_visible
        drawable.draw()

        drawable.hide()
        assert not drawable.is_visible
