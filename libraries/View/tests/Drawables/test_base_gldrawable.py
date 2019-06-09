#!/usr/bin/env python

import pytest
import sys

from qtpy.QtWidgets import QApplication

from libraries.Model.Elements.element import Element
from libraries.Model.model import Model
from libraries.View.Drawables.gldrawable import GLDrawable
from libraries.View.Drawables.meshgl import MeshGL
from libraries.View.Drawables.blockmodelgl import BlockModelGL
from libraries.View.GUI.integrableviewer import IntegrableViewer
from libraries.Model.tests.globals import *


class TestBaseDrawables:
    qt_app = QApplication(sys.argv)

    # Needed to create OpenGLWidget.context()
    widget = IntegrableViewer()
    widget.show()
    widget.hide()

    element = Element(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0])
    element.id = 0

    def test_base(self):
        assert GLDrawable(widget=IntegrableViewer(), element=self.element)

    def test_drawable_id(self):
        drawable = GLDrawable(widget=IntegrableViewer(), element=self.element)
        assert drawable.id == self.element.id

        drawable.id = 50
        assert drawable.id == 50

    def test_openglwidget_model(self):
        widget = IntegrableViewer()
        orig_model = widget.model
        widget.model = Model()
        new_model = widget.model

        assert orig_model is not new_model

    def test_openglwidget_centroid(self):
        widget = IntegrableViewer()
        assert widget.centroid == [0.0, 0.0, 0.0]

        widget.centroid = [1.0, 2.0, 3.0]
        assert widget.centroid == [1.0, 2.0, 3.0]

    def test_openglwidget_add_mesh(self):
        widget = IntegrableViewer()
        widget.mesh(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])
        widget.mesh_by_path(f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')

        assert widget.drawable_collection.__len__() == 2
        assert isinstance(widget.get_drawable(0), MeshGL)
        assert isinstance(widget.get_drawable(1), MeshGL)

    def test_openglwidget_add_wrong_mesh(self):
        widget = IntegrableViewer()

        added = widget.mesh()
        assert added is None
        assert widget.drawable_collection.__len__() == 0

        added = widget.mesh_by_path('')
        assert added is None
        assert widget.drawable_collection.__len__() == 0

    def test_openglwidget_add_block_model(self):
        widget = IntegrableViewer()
        widget.block_model(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])
        widget.block_model_by_path(f'{TEST_FILES_FOLDER_PATH}/mini.csv')

        assert widget.drawable_collection.__len__() == 2
        assert isinstance(widget.get_drawable(0), BlockModelGL)
        assert isinstance(widget.get_drawable(1), BlockModelGL)

    def test_openglwidget_add_wrong_block_model(self):
        widget = IntegrableViewer()

        added = widget.block_model()
        assert added is None
        assert widget.drawable_collection.__len__() == 0

        added = widget.block_model_by_path('')
        assert added is None
        assert widget.drawable_collection.__len__() == 0

    def test_openglwidget_drawable_visibility(self):
        widget = IntegrableViewer()
        widget.mesh(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])
        widget.block_model(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])

        assert widget.get_drawable(0).is_visible
        assert widget.get_drawable(1).is_visible

        widget.hide_drawable(1)

        assert widget.get_drawable(0).is_visible
        assert not widget.get_drawable(1).is_visible

        widget.hide_drawable(0)
        widget.show_drawable(1)

        assert not widget.get_drawable(0).is_visible
        assert widget.get_drawable(1).is_visible

        widget.show_drawable(0)
        widget.show_drawable(1)

        assert widget.get_drawable(0).is_visible
        assert widget.get_drawable(1).is_visible

    def test_openglwidget_delete_drawable(self):
        widget = IntegrableViewer()
        widget.mesh(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])
        widget.block_model(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])

        assert widget.drawable_collection.__len__() == 2
        widget.delete(0)

        assert widget.drawable_collection.__len__() == 1

        with pytest.raises(Exception):
            widget.delete(0)

        widget.delete(1)
        assert widget.drawable_collection.__len__() == 0
