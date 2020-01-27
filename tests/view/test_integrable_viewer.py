#!/usr/bin/env python

import os
import pytest

from blastsight.model.elements.element import Element
from blastsight.model.model import Model
from blastsight.view.drawables.meshgl import MeshGL
from blastsight.view.drawables.blockgl import BlockGL
from blastsight.view.drawables.pointgl import PointGL
from blastsight.view.integrableviewer import IntegrableViewer

from blastsight.controller.normalmode import NormalMode
from blastsight.controller.slicemode import SliceMode
from blastsight.controller.detectionmode import DetectionMode

from tests.globals import *


class TestIntegrableViewer:
    element = Element(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], id=0)

    def test_init(self):
        viewer = IntegrableViewer()

        assert viewer.model
        assert viewer.axis_collection
        assert viewer.background_collection
        assert viewer.drawable_collection

        assert viewer.axis
        assert viewer.bg

        assert len(viewer.controllers) > 0

        expected = [0.0, 0.0, 0.0]
        for e, r in zip(expected, viewer.rotation_angle):
            assert e == r
        for e, r in zip(expected, viewer.rotation_center):
            assert e == r

        expected = [0.0, 0.0, 200.0]
        for e, r in zip(expected, viewer.camera_position):
            assert e == r
        for e, r in zip(expected, viewer.off_center):
            assert e == r

        assert not viewer.turbo_rendering
        assert not viewer.autofit_to_screen

        assert viewer.fov == 45.0
        assert viewer.smoothness == 2.0
        assert viewer.projection_mode == 'perspective'

        assert viewer.last_id == -1
        assert viewer.last_drawable is None

    def test_model(self):
        viewer = IntegrableViewer()
        orig_model = viewer.model
        viewer.model = Model()
        new_model = viewer.model

        assert orig_model is not new_model

    def test_centroid(self):
        viewer = IntegrableViewer()
        assert viewer.rotation_center[0] == 0.0
        assert viewer.rotation_center[1] == 0.0
        assert viewer.rotation_center[2] == 0.0

        viewer.rotation_center = [1.0, 2.0, 3.0]
        assert viewer.rotation_center[0] == 1.0
        assert viewer.rotation_center[1] == 2.0
        assert viewer.rotation_center[2] == 3.0

    def test_camera(self):
        viewer = IntegrableViewer()
        for i, pos in enumerate([0.0, 0.0, 200.0]):
            assert viewer.camera_position[i] == pos
            assert viewer.off_center[i] == pos

        for i, rot in enumerate([0.0, 0.0, 0.0]):
            assert viewer.rotation_angle[i] == rot

        viewer.camera_position = [5.0, 10.0, 15.0]
        for i, pos in enumerate([5.0, 10.0, 15.0]):
            assert viewer.camera_position[i] == pos
            assert viewer.off_center[i] == pos

        viewer.rotation_angle = [90.0, 10.0, 45.0]
        for i, rot in enumerate([90.0, 10.0, 45.0]):
            assert viewer.rotation_angle[i] == rot

    def test_last_drawable(self):
        viewer = IntegrableViewer()
        assert viewer.last_id == -1

        mesh = viewer.mesh(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])
        assert viewer.last_id == 0
        assert viewer.last_drawable is mesh

    def test_update_drawable(self):
        viewer = IntegrableViewer()
        mesh = viewer.mesh(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])
        viewer.update_drawable(mesh.id)
        viewer.update_all()

        assert mesh

    def test_add_mesh(self):
        viewer = IntegrableViewer()
        viewer.mesh(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])
        viewer.mesh_by_path(f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')

        assert viewer.drawable_collection.size() == 2
        assert isinstance(viewer.get_drawable(0), MeshGL)
        assert isinstance(viewer.get_drawable(1), MeshGL)

    def test_add_wrong_mesh(self):
        viewer = IntegrableViewer()

        added = viewer.mesh()
        assert added is None
        assert viewer.drawable_collection.size() == 0

        added = viewer.mesh_by_path('')
        assert added is None
        assert viewer.drawable_collection.size() == 0

    def test_add_block_model(self):
        viewer = IntegrableViewer()
        viewer.blocks(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])
        viewer.blocks_by_path(f'{TEST_FILES_FOLDER_PATH}/mini.csv')

        assert viewer.drawable_collection.size() == 2
        assert isinstance(viewer.get_drawable(0), BlockGL)
        assert isinstance(viewer.get_drawable(1), BlockGL)

    def test_add_wrong_block_model(self):
        viewer = IntegrableViewer()

        added = viewer.blocks()
        assert added is None
        assert viewer.drawable_collection.size() == 0

        added = viewer.blocks_by_path('')
        assert added is None
        assert viewer.drawable_collection.size() == 0

    def test_add_points(self):
        viewer = IntegrableViewer()
        viewer.points(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])
        viewer.points_by_path(f'{TEST_FILES_FOLDER_PATH}/mini.csv')

        assert viewer.drawable_collection.size() == 2
        assert isinstance(viewer.get_drawable(0), PointGL)
        assert isinstance(viewer.get_drawable(1), PointGL)

    def test_add_wrong_points(self):
        viewer = IntegrableViewer()

        added = viewer.points()
        assert added is None
        assert viewer.drawable_collection.size() == 0

        added = viewer.points_by_path('')
        assert added is None
        assert viewer.drawable_collection.size() == 0

    def test_drawable_visibility(self):
        viewer = IntegrableViewer()
        viewer.mesh(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])
        viewer.blocks(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])

        assert viewer.get_drawable(0).is_visible
        assert viewer.get_drawable(1).is_visible

        viewer.hide_drawable(1)

        assert viewer.get_drawable(0).is_visible
        assert not viewer.get_drawable(1).is_visible

        viewer.hide_drawable(0)
        viewer.show_drawable(1)

        assert not viewer.get_drawable(0).is_visible
        assert viewer.get_drawable(1).is_visible

        viewer.show_drawable(0)
        viewer.show_drawable(1)

        assert viewer.get_drawable(0).is_visible
        assert viewer.get_drawable(1).is_visible

    def test_delete_drawable(self):
        viewer = IntegrableViewer()
        viewer.mesh(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])
        viewer.blocks(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])

        assert viewer.drawable_collection.size() == 2

        viewer.delete(-1)
        assert viewer.drawable_collection.size() == 2

        viewer.delete(0)
        assert viewer.drawable_collection.size() == 1

        with pytest.raises(Exception):
            viewer.delete(0)

        viewer.delete(1)
        assert viewer.drawable_collection.size() == 0

    def test_load_elements(self):
        viewer = IntegrableViewer()

        mesh = viewer.mesh(x=[-1, 1, 0],
                           y=[0, 0, 1],
                           z=[-3, -3, -3],
                           color=[0.0, 0.0, 1.0],
                           indices=[[0, 1, 2]],
                           alpha=0.4,
                           name='mesh_name',
                           extension='dxf')

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

        assert viewer.drawable_collection.size() == 5

        assert viewer.get_drawable(0) is mesh
        assert viewer.get_drawable(1) is blocks
        assert viewer.get_drawable(2) is points
        assert viewer.get_drawable(3) is lines
        assert viewer.get_drawable(4) is tubes

    def test_export(self):
        viewer = IntegrableViewer()

        mesh = viewer.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        blocks = viewer.blocks_by_path(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')

        viewer.export_mesh(f'{TEST_FILES_FOLDER_PATH}/caseron_model_export.h5m', mesh.id)
        viewer.export_blocks(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_blocks.h5p', blocks.id)
        viewer.export_points(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_points.h5p', blocks.id)
        viewer.export_lines(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_lines.h5p', blocks.id)
        viewer.export_tubes(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_tubes.h5p', blocks.id)

        # Failure deliberate
        viewer.export_mesh('a.asdf', -1)

        # Cleanup
        os.remove(f'{TEST_FILES_FOLDER_PATH}/caseron_model_export.h5m')
        os.remove(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_blocks.h5p')
        os.remove(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_points.h5p')
        os.remove(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_lines.h5p')
        os.remove(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_tubes.h5p')

        with pytest.raises(Exception):
            os.remove('a.asdf')

    def test_clear(self):
        viewer = IntegrableViewer()

        viewer.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        viewer.blocks_by_path(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')
        viewer.points_by_path(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')

        assert viewer.drawable_collection.size() == 3
        viewer.clear()
        assert viewer.drawable_collection.size() == 0

    def test_plan_north_east_view(self):
        viewer = IntegrableViewer()

        # Default
        assert viewer.rotation_angle[0] == 0.0
        assert viewer.rotation_angle[1] == 0.0
        assert viewer.rotation_angle[2] == 0.0

        # Plan
        viewer.plan_view()
        assert viewer.rotation_angle[0] == 0.0
        assert viewer.rotation_angle[1] == 0.0
        assert viewer.rotation_angle[2] == 0.0

        # North
        viewer.north_view()
        assert viewer.rotation_angle[0] == 270.0
        assert viewer.rotation_angle[1] == 0.0
        assert viewer.rotation_angle[2] == 270.0

        # East
        viewer.east_view()
        assert viewer.rotation_angle[0] == 270.0
        assert viewer.rotation_angle[1] == 0.0
        assert viewer.rotation_angle[2] == 0.0

    def test_controller_modes(self):
        viewer = IntegrableViewer()
        assert type(viewer.current_mode) is NormalMode

        viewer.set_slice_mode()
        assert type(viewer.current_mode) is SliceMode

        viewer.set_detection_mode()
        assert type(viewer.current_mode) is DetectionMode

        viewer.set_normal_mode()
        assert type(viewer.current_mode) is NormalMode

    def test_projections(self):
        viewer = IntegrableViewer()
        assert viewer.projection_mode == 'perspective'
        viewer.orthographic_projection()
        assert viewer.projection_mode == 'orthographic'
        viewer.perspective_projection()
        assert viewer.projection_mode == 'perspective'

    def test_turbo_rendering(self):
        viewer = IntegrableViewer()
        viewer.mesh(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])

        assert not viewer.last_drawable.is_boostable
        viewer.turbo_rendering = True
        assert viewer.last_drawable.is_boostable

        viewer.turbo_rendering = False
        assert not viewer.last_drawable.is_boostable

    def test_fit_camera(self):
        viewer = IntegrableViewer()

        assert viewer.off_center[2] == 200.0
        viewer.fit_to_screen()  # No drawables, no fit
        assert viewer.off_center[2] == 200.0

        viewer.mesh(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])

        assert not viewer.autofit_to_screen
        viewer.autofit_to_screen = True

        assert viewer.off_center[2] != 200.0

        viewer.camera_position = [0.0, 0.0, 200.0]
        viewer.camera_at(viewer.last_id)

        assert viewer.off_center[2] != 200.0

        viewer.camera_position = [0.0, 0.0, 200.0]
        viewer.projection_mode = 'orthographic'

        viewer.fit_to_bounds(*viewer.last_drawable.element.bounding_box)
        assert viewer.off_center[2] != 200.0

        viewer.resizeGL(viewer.width(), viewer.height())

    def test_load_folder(self):
        viewer = IntegrableViewer()
        meshes = viewer.meshes_by_folder_path(f'{TEST_FILES_FOLDER_PATH}')

        failure = viewer.blocks_by_folder_path(f'{TEST_FILES_FOLDER_PATH}/../blastsight')
        assert len(failure) == 0
        failure = viewer.points_by_folder_path(f'{TEST_FILES_FOLDER_PATH}/../blastsight')
        assert len(failure) == 0
        failure = viewer.lines_by_folder_path(f'{TEST_FILES_FOLDER_PATH}/../blastsight')
        assert len(failure) == 0
        failure = viewer.tubes_by_folder_path(f'{TEST_FILES_FOLDER_PATH}/../blastsight')
        assert len(failure) == 0

        assert viewer.drawable_collection.size() == len(meshes) > 0

        assert viewer.drawable_collection.size() == len(failure) + len(meshes)

    def test_screen_to_ndc(self):
        viewer = IntegrableViewer()
        viewer.resize(800, 600)
        ndc = viewer.screen_to_ndc(400, 150, 0)

        expected = [0.0, 0.5, 1.0]
        for e, r in zip(expected, ndc):
            assert e == r

    def test_unproject(self):
        viewer = IntegrableViewer()
        viewer.resize(800, 600)

        expected = [0.0, 0.0, -1.0]
        for e, r in zip(expected, viewer.unproject(400, 300, 0, viewer.world, viewer.camera, viewer.proj)):
            assert e == r

        assert viewer.unproject(500, 300, 0, viewer.world, viewer.camera, viewer.proj)[0] > 0.0
        assert viewer.unproject(500, 400, 0, viewer.world, viewer.camera, viewer.proj)[1] < 0.0
