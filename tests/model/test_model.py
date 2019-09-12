#!/usr/bin/env python

import os
import pytest
from minevis.model.parsers.offparser import OFFParser
from minevis.model.parsers.csvparser import CSVParser
from minevis.model.model import Model
from tests.globals import *


class TestModel:
    # Mesh
    def test_add_mesh(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/caseron.off'
        info = OFFParser.load_file(path)
        vertices = info.vertices
        indices = info.indices

        x, y, z = zip(*vertices)

        mesh_1 = model.mesh(vertices=vertices, indices=indices, name='caseron', extension='off')
        mesh_2 = model.mesh(x=x, y=y, z=z, indices=indices, name='caseron', extension='off')

        assert mesh_1.id != mesh_2.id

    def test_add_mesh_by_path(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/caseron.dxf'

        mesh_1 = model.mesh_by_path(path=path)
        mesh_2 = model.mesh_by_path(path=path)

        assert mesh_1.id != mesh_2.id
        assert mesh_1.name == 'caseron'
        assert mesh_1.extension == 'dxf'

    def test_wrong_mesh(self):
        model = Model()
        with pytest.raises(Exception):
            model.mesh_by_path(f'{TEST_FILES_FOLDER_PATH}/nonexistent.off')

    def test_get_mesh(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/caseron.off'
        info = OFFParser.load_file(path)
        vertices = info.vertices
        indices = info.indices

        mesh = model.mesh(vertices=vertices, indices=indices)
        mesh_get = model.get(mesh.id)

        assert mesh is not None
        assert mesh_get is not None
        assert mesh.id == mesh_get.id

    def test_delete_mesh(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/caseron.off'
        info = OFFParser.load_file(path)
        vertices = info.vertices
        indices = info.indices

        mesh = model.mesh(vertices=vertices, indices=indices)
        id_ = mesh.id
        model.delete(id_)

        with pytest.raises(Exception):
            model.get(id_)

    # Block model
    def test_add_block_model(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'
        info = CSVParser.load_file(path)
        data = info.data

        bm_1 = model.blocks(data=data)
        bm_2 = model.blocks(data=data)

        assert bm_1.id != bm_2.id

    def test_add_blockmodel_by_path(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'

        bm_1 = model.blocks_by_path(path=path)
        bm_2 = model.blocks_by_path(path=path)

        assert bm_1.id != bm_2.id

    def test_wrong_blockmodel(self):
        model = Model()
        with pytest.raises(Exception):
            model.blocks_by_path(f'{TEST_FILES_FOLDER_PATH}/nonexistent.csv')

    def test_get_blockmodel(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'
        info = CSVParser.load_file(path)
        data = info.data

        bm = model.blocks(data=data)
        bm_get = model.get(bm.id)

        assert bm is not None
        assert bm_get is not None
        assert bm.id == bm_get.id

    def test_delete_blockmodel(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'
        info = CSVParser.load_file(path)
        data = info.data

        bm = model.blocks(data=data)
        id_ = bm.id
        model.delete(id_)

        with pytest.raises(Exception):
            model.get(id_)

    # Lines
    def test_add_lines(self):
        model = Model()
        vertices = [[-0.5, -2.0, -0.0],
                    [0.5, 1.5, 0.0]]

        color = [1.0, 0.0, 0.0]
        x, y, z = zip(*vertices)

        lines_1 = model.lines(vertices=vertices, color=color)
        lines_2 = model.lines(x=x, y=y, z=z, color=color)

        assert lines_1.id != lines_2.id

    def test_get_lines(self):
        model = Model()
        vertices = [[-0.5, -2.0, -0.0],
                    [0.5, 1.5, 0.0]]

        color = [1.0, 0.0, 0.0]

        lines = model.lines(vertices=vertices, color=color)
        lines_get = model.get(lines.id)

        assert lines is not None
        assert lines_get is not None
        assert lines.id == lines_get.id

    def test_delete_lines(self):
        model = Model()
        vertices = [[-0.5, -2.0, -0.0],
                    [0.5, 1.5, 0.0]]

        color = [1.0, 0.0, 0.0]

        lines = model.lines(vertices=vertices, color=color)

        id_ = lines.id
        model.delete(id_)

        with pytest.raises(Exception):
            model.get(id_)

    # Tubes
    def test_add_tubes(self):
        model = Model()
        vertices = [[-0.5, -2.0, -0.0],
                    [0.5, 1.5, 0.0]]

        color = [1.0, 0.0, 0.0]
        x, y, z = zip(*vertices)

        tubes_1 = model.tubes(vertices=vertices, color=color)
        tubes_2 = model.tubes(x=x, y=y, z=z, color=color)

        assert tubes_1.id != tubes_2.id

    def test_get_tubes(self):
        model = Model()
        vertices = [[-0.5, -2.0, -0.0],
                    [0.5, 1.5, 0.0]]

        color = [1.0, 0.0, 0.0]

        tubes = model.tubes(vertices=vertices, color=color)
        tubes_get = model.get(tubes.id)

        assert tubes is not None
        assert tubes_get is not None
        assert tubes.id == tubes_get.id

    def test_delete_tubes(self):
        model = Model()
        vertices = [[-0.5, -2.0, -0.0],
                    [0.5, 1.5, 0.0]]

        color = [1.0, 0.0, 0.0]

        tubes = model.tubes(vertices=vertices, color=color)

        id_ = tubes.id
        model.delete(id_)

        with pytest.raises(Exception):
            model.get(id_)

    # Points
    def test_add_points(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'
        info = CSVParser.load_file(path)
        data = info.data

        bm_1 = model.points(data=data)
        bm_2 = model.points(data=data)

        assert bm_1.id != bm_2.id

    def test_add_points_by_path(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'

        bm_1 = model.points_by_path(path=path)
        bm_2 = model.points_by_path(path=path)

        assert bm_1.id != bm_2.id

    def test_wrong_points(self):
        model = Model()
        with pytest.raises(Exception):
            model.points_by_path(f'{TEST_FILES_FOLDER_PATH}/nonexistent.csv')

    def test_get_points(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'
        info = CSVParser.load_file(path)
        data = info.data

        bm = model.points(data=data)
        bm_get = model.get(bm.id)

        assert bm is not None
        assert bm_get is not None
        assert bm.id == bm_get.id

    def test_delete_points(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'
        info = CSVParser.load_file(path)
        data = info.data

        bm = model.points(data=data)
        id_ = bm.id
        model.delete(id_)

        with pytest.raises(Exception):
            model.get(id_)

    # Multiple
    def test_add_multiple(self):
        model = Model()
        elem_1 = model.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        elem_2 = model.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')
        elem_3 = model.blocks_by_path(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')

        assert elem_1.id != elem_2.id != elem_3.id

    def test_get_multiple(self):
        model = Model()
        elem_1 = model.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        elem_2 = model.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')
        elem_3 = model.blocks_by_path(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')

        assert type(elem_1) == type(elem_2)
        assert type(elem_2) != type(elem_3)

        elem_get_1 = model.get(elem_1.id)
        elem_get_2 = model.get(elem_2.id)
        elem_get_3 = model.get(elem_3.id)

        assert type(elem_get_1) == type(elem_get_2)
        assert type(elem_get_2) != type(elem_get_3)

    def test_collection(self):
        model = Model()

        assert model.last_id == -1
        model.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        assert model.last_id == 0
        model.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')
        assert model.last_id == 1
        model.blocks_by_path(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')
        assert model.last_id == 2

        assert len(model.element_collection) == 3
        assert len(model.mesh_collection) == 2
        assert len(model.block_model_collection) == 1

    def test_export(self):
        model = Model()
        mesh = model.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        blocks = model.blocks_by_path(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')
        points = model.points_by_path(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')

        model.export_mesh(f'{TEST_FILES_FOLDER_PATH}/caseron_model_export.h5m', mesh.id)
        model.export_blocks(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_blocks.h5p', blocks.id)
        model.export_points(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_points.h5p', points.id)

        # Cleanup
        os.remove(f'{TEST_FILES_FOLDER_PATH}/caseron_model_export.h5m')
        os.remove(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_blocks.h5p')
        os.remove(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_points.h5p')
