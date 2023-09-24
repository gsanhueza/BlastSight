#!/usr/bin/env python

import os
import pytest

from blastsight.model.elements.element import Element
from blastsight.model.model import Model

from blastsight.view.drawables.meshgl import MeshGL
from blastsight.view.drawables.blockgl import BlockGL
from blastsight.view.drawables.pointgl import PointGL
from blastsight.view.drawables.linegl import LineGL
from blastsight.view.drawables.tubegl import TubeGL

from blastsight.view.integrableviewer import IntegrableViewer

from blastsight.interactors.normal_interactor import NormalInteractor
from blastsight.interactors.slice_interactor import SliceInteractor
from blastsight.interactors.detect_interactor import DetectInteractor

from tests.globals import *


class TestIntegrableViewer:
    element = Element(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], id=0)

    @staticmethod
    def equal_list(la, lb) -> bool:
        for a, b in zip(la, lb):
            if a != b:
                return False
        return True

    def test_init(self):
        viewer = IntegrableViewer()

        assert viewer.model
        assert viewer.post_collection
        assert viewer.pre_collection
        assert viewer.drawable_collection

        assert viewer.axis
        assert viewer.background

        assert len(viewer.interactors) > 0

        expected = [0.0, 0.0, 0.0]
        assert self.equal_list(expected, viewer.rotation_angle)
        assert self.equal_list(expected, viewer.rotation_center)

        expected = [0.0, 0.0, 200.0]
        assert self.equal_list(expected, viewer.camera_position)

        assert viewer.fov == 45.0
        assert viewer.smoothness == 2.0
        assert viewer.current_projection == 'Perspective'

        assert viewer.last_id == -1
        assert viewer.last_drawable is None

    def test_model(self):
        viewer = IntegrableViewer()
        orig_model = viewer.model
        viewer.model = Model()
        new_model = viewer.model

        assert orig_model is not new_model

    def test_camera_position(self):
        viewer = IntegrableViewer()

        # Translate camera
        translation = [5.0, 10.0, 15.0]

        assert self.equal_list([0.0, 0.0, 200.0], viewer.get_camera_position())
        viewer.translate(*translation)
        assert self.equal_list([5.0, 10.0, 215.0], viewer.get_camera_position())
        viewer.translate(*translation)
        assert self.equal_list([10.0, 20.0, 230.0], viewer.get_camera_position())

        viewer.set_camera_position(translation)
        assert self.equal_list(translation, viewer.get_camera_position())

    def test_camera_rotation(self):
        viewer = IntegrableViewer()

        # Rotate camera
        rotation = [90.0, 10.0, 45.0]

        assert self.equal_list([0.0, 0.0, 0.0], viewer.get_rotation_angle())
        viewer.rotate(*rotation)
        assert self.equal_list([90.0, 10.0, 45.0], viewer.get_rotation_angle())
        viewer.rotate(*rotation)
        assert self.equal_list([180.0, 20.0, 90.0], viewer.get_rotation_angle())

        viewer.set_rotation_angle(rotation)
        assert self.equal_list(rotation, viewer.get_rotation_angle())

    def test_center_position(self):
        viewer = IntegrableViewer()

        # Translate center
        center = [10.0, 20.0, 30.0]

        assert self.equal_list([0.0, 0.0, 0.0], viewer.get_rotation_center())
        viewer.translate_center(*center)
        assert self.equal_list([10.0, 20.0, 30.0], viewer.get_rotation_center())
        viewer.translate_center(*center)
        assert self.equal_list([20.0, 40.0, 60.0], viewer.get_rotation_center())

        viewer.set_rotation_center(center)
        assert self.equal_list(center, viewer.get_rotation_center())

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

    def test_add_elements(self):
        viewer = IntegrableViewer()

        # Mesh
        mesh = viewer.mesh(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])
        assert type(mesh) is MeshGL
        assert viewer.last_id == mesh.id
        assert viewer.last_drawable is mesh
        assert len(viewer.get_all_drawables()) == 1

        # Blocks
        blocks = viewer.blocks(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])
        assert type(blocks) is BlockGL
        assert viewer.last_id == blocks.id
        assert viewer.last_drawable is blocks
        assert len(viewer.get_all_drawables()) == 2

        # Points
        points = viewer.points(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])
        assert type(points) is PointGL
        assert viewer.last_id == points.id
        assert viewer.last_drawable is points
        assert len(viewer.get_all_drawables()) == 3

        # Lines
        lines = viewer.lines(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0])
        assert type(lines) is LineGL
        assert viewer.last_id == lines.id
        assert viewer.last_drawable is lines
        assert len(viewer.get_all_drawables()) == 4

        # Tubes
        tubes = viewer.tubes(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0])
        assert type(tubes) is TubeGL
        assert viewer.last_id == tubes.id
        assert viewer.last_drawable is tubes
        assert len(viewer.get_all_drawables()) == 5

    def test_load_elements(self):
        viewer = IntegrableViewer()

        # Mesh
        mesh = viewer.load_mesh(f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')
        assert type(mesh) is MeshGL
        assert viewer.last_id == mesh.id
        assert viewer.last_drawable is mesh
        assert len(viewer.get_all_drawables()) == 1

        # Blocks
        blocks = viewer.load_blocks(f'{TEST_FILES_FOLDER_PATH}/mini.csv')
        assert type(blocks) is BlockGL
        assert viewer.last_id == blocks.id
        assert viewer.last_drawable is blocks
        assert len(viewer.get_all_drawables()) == 2

        # Points
        points = viewer.load_points(f'{TEST_FILES_FOLDER_PATH}/mini.csv')
        assert type(points) is PointGL
        assert viewer.last_id == points.id
        assert viewer.last_drawable is points
        assert len(viewer.get_all_drawables()) == 3

        # Lines
        lines = viewer.load_lines(f'{TEST_FILES_FOLDER_PATH}/mini.csv')
        assert type(lines) is LineGL
        assert viewer.last_id == lines.id
        assert viewer.last_drawable is lines
        assert len(viewer.get_all_drawables()) == 4

        # Tubes
        tubes = viewer.load_tubes(f'{TEST_FILES_FOLDER_PATH}/mini.csv')
        assert type(tubes) is TubeGL
        assert viewer.last_id == tubes.id
        assert viewer.last_drawable is tubes
        assert len(viewer.get_all_drawables()) == 5

    def test_load_multiple(self):
        viewer = IntegrableViewer()
        path = f'{TEST_FILES_FOLDER_PATH}/caseron.dxf'
        path_list = 3 * [path]

        meshes = viewer.load_multiple([], viewer.load_mesh)
        assert len(meshes) == 0
        assert len(viewer.get_all_ids()) == 0

        meshes = viewer.load_multiple(path_list, viewer.load_mesh)
        assert len(path_list) == len(meshes)
        assert len(viewer.get_all_ids()) == len(path_list)

        for mesh in meshes:
            assert type(mesh) is MeshGL

    def test_add_wrong_elements(self):
        viewer = IntegrableViewer()

        assert viewer.mesh() is None
        assert viewer.blocks() is None
        assert viewer.points() is None
        assert viewer.lines() is None
        assert viewer.tubes() is None

        assert viewer.load_mesh('') is None
        assert viewer.load_blocks('') is None
        assert viewer.load_points('') is None
        assert viewer.load_lines('') is None
        assert viewer.load_tubes('') is None

        assert len(viewer.get_all_drawables()) == 0

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

        mesh = viewer.load_mesh(path=f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        blocks = viewer.load_blocks(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')

        viewer.export_element(f'{TEST_FILES_FOLDER_PATH}/caseron_model_export.h5m', mesh.id)
        viewer.export_element(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_blocks.h5p', blocks.id)
        viewer.export_element(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_points.h5p', blocks.id)
        viewer.export_element(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_lines.h5p', blocks.id)
        viewer.export_element(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_tubes.h5p', blocks.id)

        # Failure deliberate
        viewer.export_element('a.asdf', -1)

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

        viewer.load_mesh(path=f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        viewer.load_blocks(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')
        viewer.load_points(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')

        assert viewer.drawable_collection.size() == 3
        viewer.clear()
        assert viewer.drawable_collection.size() == 0

    def test_plan_north_east_view(self):
        viewer = IntegrableViewer()

        # Default
        expected = [0.0, 0.0, 0.0]
        assert self.equal_list(expected, viewer.rotation_angle)

        # Plan
        viewer.plan_view()
        expected = [0.0, 0.0, 0.0]
        assert self.equal_list(expected, viewer.rotation_angle)

        # North
        viewer.north_view()
        expected = [270.0, 0.0, 270.0]
        assert self.equal_list(expected, viewer.rotation_angle)

        # East
        viewer.east_view()
        expected = [270.0, 0.0, 0.0]
        assert self.equal_list(expected, viewer.rotation_angle)

    def test_interactor_modes(self):
        viewer = IntegrableViewer()
        assert type(viewer.current_interactor) is NormalInteractor

        viewer.set_slice_interactor()
        assert type(viewer.current_interactor) is SliceInteractor

        viewer.set_detection_interactor()
        assert type(viewer.current_interactor) is DetectInteractor

        viewer.set_normal_interactor()
        assert type(viewer.current_interactor) is NormalInteractor

    def test_projections(self):
        viewer = IntegrableViewer()
        assert viewer.current_projection == 'Perspective'
        viewer.orthographic_projection()
        assert viewer.current_projection == 'Orthographic'
        viewer.perspective_projection()
        assert viewer.current_projection == 'Perspective'

    def test_turbo_rendering(self):
        viewer = IntegrableViewer()
        viewer.mesh(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])

        assert not viewer.last_drawable.is_boostable
        viewer.set_turbo_rendering(True)
        assert viewer.last_drawable.is_boostable

        viewer.set_turbo_rendering(False)
        assert not viewer.last_drawable.is_boostable

    def test_resize_gl(self):
        viewer = IntegrableViewer()

        expected = viewer.proj_matrix.data()
        assert self.equal_list(expected, viewer.proj_matrix.data())

        viewer.resizeGL(10, 10)
        perspective = viewer.proj_matrix.data()
        assert not self.equal_list(expected, perspective)

        viewer.orthographic_projection()
        viewer.resizeGL(10, 10)
        orthographic = viewer.proj_matrix.data()

        assert not self.equal_list(expected, orthographic)
        assert not self.equal_list(perspective, orthographic)

    def test_fit_camera(self):
        viewer = IntegrableViewer()

        expected = [0.0, 0.0, 200.0]
        assert self.equal_list(expected, viewer.off_center)
        viewer.fit_to_screen()  # No drawables, no fit
        assert self.equal_list(expected, viewer.off_center)

        viewer.mesh(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])

        viewer.fit_to_screen()  # One drawable, auto-fit
        assert not self.equal_list(expected, viewer.off_center)

        viewer.camera_position = expected
        viewer.camera_at(viewer.last_id)
        viewer.current_projection = 'orthographic'

        viewer.fit_to_bounds(*viewer.last_drawable.element.bounding_box)
        assert not self.equal_list(expected, viewer.off_center)

    def test_load_folder(self):
        viewer = IntegrableViewer()
        successes = []
        failures = []

        successes += viewer.load_mesh_folder(f'{TEST_FILES_FOLDER_PATH}')
        assert len(successes) > 0
        failures += viewer.load_blocks_folder(f'{TEST_FILES_FOLDER_PATH}/../blastsight')
        assert len(failures) == 0
        failures += viewer.load_points_folder(f'{TEST_FILES_FOLDER_PATH}/../blastsight')
        assert len(failures) == 0
        failures += viewer.load_lines_folder(f'{TEST_FILES_FOLDER_PATH}/../blastsight')
        assert len(failures) == 0
        failures += viewer.load_tubes_folder(f'{TEST_FILES_FOLDER_PATH}/../blastsight')
        assert len(failures) == 0

        assert viewer.drawable_collection.size() == len(successes) > 0
        assert viewer.drawable_collection.size() == len(failures) + len(successes)

    def test_screen_to_ndc(self):
        viewer = IntegrableViewer()
        viewer.resize(800, 600)
        ndc = viewer.screen_to_ndc(400, 150, 0)

        expected = [0.0, 0.5, 1.0]
        assert self.equal_list(expected, ndc)

    def test_unproject(self):
        viewer = IntegrableViewer()

        expected = [0.0, 0.0, -1.0]
        unproject = viewer.unproject(0, 0, 0)
        assert self.equal_list(expected, unproject)

        assert viewer.unproject(0.5, 0.0, 0)[0] > 0.0
        assert viewer.unproject(-0.5, 0.0, 0)[0] < 0.0

    def test_ray_from_click(self):
        viewer = IntegrableViewer()
        viewer.resize(800, 600)

        # Perspective: Ray deviates when click is not at center
        expected = [0.0, 0.0, -1.0]
        ray = viewer.ray_from_click(400, 300, 0)
        assert self.equal_list(expected, ray)

        ray = viewer.ray_from_click(100, 100, 0)
        assert not self.equal_list(expected, ray)

        # Orthographic: Ray always has the same direction
        viewer.orthographic_projection()
        ray = viewer.ray_from_click(400, 300, 0)
        assert self.equal_list(expected, ray)

        ray = viewer.ray_from_click(100, 100, 0)
        assert self.equal_list(expected, ray)

    def test_origin_from_click(self):
        viewer = IntegrableViewer()
        viewer.resize(800, 600)

        # Perspective: The origin doesn't change, only the ray
        expected = [0.0, 0.0, 0.0]
        origin = viewer.origin_from_click(100, 100, 0)
        assert self.equal_list(expected, origin)

        # Orthographic: The ray doesn't change, but the origin does
        viewer.orthographic_projection()
        origin = viewer.origin_from_click(100, 100, 0)
        assert not self.equal_list(expected, origin)

    def test_get_normal(self):
        viewer = IntegrableViewer()

        # Auto-generates a normal from 2 rays and 2 origins
        normal = viewer.get_normal(origin_list=[[0.0, 0.0, 0.0],
                                                [100.0, 0.0, 0.0]],
                                   ray_list=[[-0.5, 0.0, -0.7],
                                             [+0.5, 0.0, -0.7]])

        # Perspective: We only need the rays
        expected = [0.0, -1.0, 0.0]
        assert self.equal_list(expected, normal)

        # Orthographic: A origin is needed to make differences between the rays
        viewer.orthographic_projection()
        normal = viewer.get_normal(origin_list=[[0.0, 100.0, 0.0],
                                                [100.0, 0.0, 0.0]],
                                   ray_list=[[-0.5, 0.0, -0.7],
                                             [+0.5, 0.0, -0.7]])

        assert not self.equal_list(expected, normal)

    def test_angles_from_vectors(self):
        viewer = IntegrableViewer()

        # Make the normal face the camera
        default = [0.0, 0.0, 0.0]
        expected = [-90.0, 0.0, -90.0]

        normal = [1.0, 0.0, 0.0]
        up = [0.0, 0.0, 1.0]
        angles = viewer.angles_from_vectors(normal, up)
        assert self.equal_list(expected, angles)

        assert self.equal_list(default, viewer.get_rotation_angle())
        viewer.set_camera_from_vectors(normal, up)
        assert self.equal_list(expected, viewer.get_rotation_angle())

    def test_generate_slice_description(self):
        def on_description(description: dict):
            assert 'origin' in description.keys()
            assert 'normal' in description.keys()
            assert 'up' in description.keys()

        viewer = IntegrableViewer()
        viewer.signal_slice_description.connect(on_description)

        viewer.generate_slice_description(origin_list=[[0.0, 0.0, 0.0],
                                                       [100.0, 0.0, 0.0]],
                                          ray_list=[[-0.5, 0.0, -0.7],
                                                    [+0.5, 0.0, -0.7]])

    def test_slice_meshes(self):
        viewer = IntegrableViewer()
        mesh = viewer.load_mesh(f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')
        mesh.hide()

        origin = mesh.center
        normal = [0.0, 0.6, 0.8]
        slices = viewer.slice_meshes(origin, normal, include_hidden=False)
        assert len(slices) == 0

        slices = viewer.slice_meshes(origin, normal, include_hidden=True)
        assert len(slices) > 0

    def test_slice_blocks(self):
        viewer = IntegrableViewer()
        blocks = viewer.load_blocks(f'{TEST_FILES_FOLDER_PATH}/mini.csv')
        blocks.hide()

        origin = blocks.center
        normal = [0.0, 0.6, -0.8]
        slices = viewer.slice_blocks(origin, normal, include_hidden=False)
        assert len(slices) == 0

        slices = viewer.slice_blocks(origin, normal, include_hidden=True)
        assert len(slices) > 0
