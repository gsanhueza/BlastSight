#!/usr/bin/env python

import pytest

from minevis.model.elements.element import Element
from minevis.model.model import Model
from minevis.view.drawables.meshgl import MeshGL
from minevis.view.drawables.blockgl import BlockGL
from minevis.view.drawables.pointgl import PointGL
from minevis.view.gui.integrableviewer import IntegrableViewer
from minevis.model.tests.globals import *


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
        widget.blocks(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])
        widget.block_model_by_path(f'{TEST_FILES_FOLDER_PATH}/mini.csv')

        assert widget.drawable_collection.__len__() == 2
        assert isinstance(widget.get_drawable(0), BlockGL)
        assert isinstance(widget.get_drawable(1), BlockGL)

    def test_integrable_viewer_add_wrong_block_model(self):
        widget = IntegrableViewer()

        added = widget.blocks()
        assert added is None
        assert widget.drawable_collection.__len__() == 0

        added = widget.block_model_by_path('')
        assert added is None
        assert widget.drawable_collection.__len__() == 0

    def test_integrable_viewer_add_points(self):
        widget = IntegrableViewer()
        widget.points(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])
        widget.points_by_path(f'{TEST_FILES_FOLDER_PATH}/mini.csv')

        assert widget.drawable_collection.__len__() == 2
        assert isinstance(widget.get_drawable(0), PointGL)
        assert isinstance(widget.get_drawable(1), PointGL)

    def test_integrable_viewer_add_wrong_points(self):
        widget = IntegrableViewer()

        added = widget.points()
        assert added is None
        assert widget.drawable_collection.__len__() == 0

        added = widget.points_by_path('')
        assert added is None
        assert widget.drawable_collection.__len__() == 0

    def test_integrable_viewer_drawable_visibility(self):
        widget = IntegrableViewer()
        widget.mesh(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])
        widget.blocks(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])

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
        widget.blocks(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])

        assert widget.drawable_collection.__len__() == 2
        widget.delete(0)

        assert widget.drawable_collection.__len__() == 1

        with pytest.raises(Exception):
            widget.delete(0)

        widget.delete(1)
        assert widget.drawable_collection.__len__() == 0

    def test_load_elements(self):
        viewer = IntegrableViewer()

        mesh = viewer.mesh(x=[-1, 1, 0],
                           y=[0, 0, 1],
                           z=[-3, -3, -3],
                           color=[0.0, 0.0, 1.0],
                           indices=[[0, 1, 2]],
                           alpha=0.4,
                           name='mesh_name',
                           ext='dxf')

        assert viewer.last_id == 0

        blocks = viewer.blocks(x=[-3, 3, 0],
                               y=[0, 0, 5],
                               z=[0, 0, 0],
                               block_size=[1.0, 1.0, 1.0],
                               values=[0.5, 1.0, 1.5])

        assert viewer.last_id == 1

        points = viewer.points(vertices=[[-3, 2, 0],
                                         [0, 2, 1],
                                         [3, 2, 2]],
                               point_size=10.0,
                               values=[1.5, 1.0, 0.5])

        assert viewer.last_id == 2

        lines = viewer.lines(x=[-0.5, 0.5],
                             y=[-2.0, 1.5],
                             z=[-2.0, -2.0],
                             color=[0.2, 0.8, 0.8])

        assert viewer.last_id == 3

        tubes = viewer.tubes(x=[0.5, -0.5, 1.5, 1.5],
                             y=[-2.0, 1.8, 1.8, 0.0],
                             z=[-1.5, -1.5, -1.5, -1.5],
                             color=[0.9, 0.2, 0.2],
                             radius=0.2,
                             resolution=15)

        assert viewer.last_id == 4

        assert len(viewer.drawable_collection) == 5

        assert viewer.get_drawable(0) is mesh
        assert viewer.get_drawable(1) is blocks
        assert viewer.get_drawable(2) is points
        assert viewer.get_drawable(3) is lines
        assert viewer.get_drawable(4) is tubes
