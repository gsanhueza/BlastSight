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


class TestIntegrableViewer:
    element = Element(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0])
    element.id = 0

    def test_integrable_viewer_model(self):
        widget = IntegrableViewer()
        orig_model = widget.model
        widget.model = Model()
        new_model = widget.model

        assert orig_model is not new_model

    def test_integrable_viewer_centroid(self):
        widget = IntegrableViewer()
        assert widget.centroid == [0.0, 0.0, 0.0]

        widget.centroid = [1.0, 2.0, 3.0]
        assert widget.centroid == [1.0, 2.0, 3.0]

    def test_integrable_viewer_camera(self):
        widget = IntegrableViewer()
        assert widget.camera_position[0] == 0.0
        assert widget.camera_position[1] == 0.0
        assert widget.camera_position[2] == 200.0

        assert widget.camera_rotation[0] == 0.0
        assert widget.camera_rotation[1] == 0.0
        assert widget.camera_rotation[2] == 0.0

        widget.camera_position = [5.0, 10.0, 15.0]
        assert widget.camera_position[0] == 5.0
        assert widget.camera_position[1] == 10.0
        assert widget.camera_position[2] == 15.0

        widget.camera_rotation = [90.0, 10.0, 45.0]
        assert widget.camera_rotation[0] == 90.0
        assert widget.camera_rotation[1] == 10.0
        assert widget.camera_rotation[2] == 45.0

    def test_integrable_viewer_last_id(self):
        widget = IntegrableViewer()
        assert widget.last_id == -1

        widget.mesh(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])
        assert widget.last_id == 0

    def test_integrable_viewer_add_mesh(self):
        widget = IntegrableViewer()
        widget.mesh(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])
        widget.mesh_by_path(f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')

        assert widget.drawable_collection.__len__() == 2
        assert isinstance(widget.get_drawable(0), MeshGL)
        assert isinstance(widget.get_drawable(1), MeshGL)

    def test_integrable_viewer_add_wrong_mesh(self):
        widget = IntegrableViewer()

        added = widget.mesh()
        assert added is None
        assert widget.drawable_collection.__len__() == 0

        added = widget.mesh_by_path('')
        assert added is None
        assert widget.drawable_collection.__len__() == 0

    def test_integrable_viewer_add_block_model(self):
        widget = IntegrableViewer()
        widget.block_model(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])
        widget.block_model_by_path(f'{TEST_FILES_FOLDER_PATH}/mini.csv')

        assert widget.drawable_collection.__len__() == 2
        assert isinstance(widget.get_drawable(0), BlockModelGL)
        assert isinstance(widget.get_drawable(1), BlockModelGL)

    def test_integrable_viewer_add_wrong_block_model(self):
        widget = IntegrableViewer()

        added = widget.block_model()
        assert added is None
        assert widget.drawable_collection.__len__() == 0

        added = widget.block_model_by_path('')
        assert added is None
        assert widget.drawable_collection.__len__() == 0

    def test_integrable_viewer_drawable_visibility(self):
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

    def test_integrable_viewer_delete_drawable(self):
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
