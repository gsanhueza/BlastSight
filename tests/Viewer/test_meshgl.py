#!/usr/bin/env python

import sys
import pytest
from View.GUI.openglwidget import OpenGLWidget
from View.Drawables.meshgl import MeshGL
from Model.Elements.meshelement import MeshElement

from PyQt5.QtWidgets import QApplication


class TestMeshGL:
    qt_app = QApplication(sys.argv)
    widget = OpenGLWidget()

    # Needed to create OpenGLWidget.context()
    widget.show()
    widget.hide()

    element = MeshElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])
    element.id = 0

    def test_empty_meshgl(self):
        with pytest.raises(Exception):
            MeshGL()

    def test_meshgl_no_widget(self):
        widget = None
        element = MeshElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])
        element.id = 0

        with pytest.raises(Exception):
            MeshGL(widget=widget, element=element)

    def test_meshgl_base(self):
        drawable = MeshGL(widget=self.widget, element=self.element)

        assert drawable
        assert drawable.id == 0
        assert isinstance(drawable.widget, OpenGLWidget)

        assert not drawable.is_initialized

    def test_meshgl_initialize(self):
        drawable = MeshGL(widget=self.widget, element=self.element)
        assert not drawable.is_initialized

        drawable.initialize()

        assert drawable.is_initialized
