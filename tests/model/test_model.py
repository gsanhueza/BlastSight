#!/usr/bin/env python

import os
import pytest
from blastsight.model.parsers.offparser import OFFParser
from blastsight.model.parsers.csvparser import CSVParser
from blastsight.model.model import Model
from tests.globals import *


class TestModel:
    def test_paths_from_directory(self):
        model = Model()
        paths = model.get_paths_from_directory(f'{TEST_FILES_FOLDER_PATH}')

        assert len(paths) > 0

    # Mesh
    def test_add_mesh(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/caseron.off'
        info = OFFParser.load_file(path)
        vertices = info.get('data').get('vertices')
        indices = info.get('data').get('indices')

        x, y, z = zip(*vertices)

        mesh_1 = model.mesh(vertices=vertices, indices=indices, name='caseron', extension='off')
        mesh_2 = model.mesh(x=x, y=y, z=z, indices=indices, name='caseron', extension='off')

        assert mesh_1.id != mesh_2.id

    def test_load_mesh(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/caseron.dxf'

        mesh_1 = model.load_mesh(path=path)
        mesh_2 = model.load_mesh(path=path)

        assert mesh_1.id != mesh_2.id
        assert mesh_1.name == 'caseron'
        assert mesh_1.extension == 'dxf'

    def test_wrong_mesh(self):
        model = Model()
        with pytest.raises(Exception):
            model.load_mesh(f'{TEST_FILES_FOLDER_PATH}/nonexistent.off')

    def test_get_mesh(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/caseron.off'
        info = OFFParser.load_file(path)
        vertices = info.get('data').get('vertices')
        indices = info.get('data').get('indices')

        mesh = model.mesh(vertices=vertices, indices=indices)
        mesh_get = model.get(mesh.id)

        assert mesh is not None
        assert mesh_get is not None
        assert mesh.id == mesh_get.id

    def test_delete_mesh(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/caseron.off'
        info = OFFParser.load_file(path)
        vertices = info.get('data').get('vertices')
        indices = info.get('data').get('indices')

        mesh = model.mesh(vertices=vertices, indices=indices)
        _id = mesh.id
        model.delete(_id)

        assert model.get(_id) is None

    # Block model
    def test_add_blocks(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'
        info = CSVParser.load_file(path)
        data = info.get('data')

        bm_1 = model.blocks(data=data)
        bm_2 = model.blocks(data=data)

        assert bm_1.id != bm_2.id

    def test_load_blocks(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'

        bm_1 = model.load_blocks(path=path)
        bm_2 = model.load_blocks(path=path)

        assert bm_1.id != bm_2.id

    def test_wrong_blocks(self):
        model = Model()
        with pytest.raises(Exception):
            model.load_blocks(f'{TEST_FILES_FOLDER_PATH}/nonexistent.csv')

    def test_get_blocks(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'
        info = CSVParser.load_file(path)
        data = info.get('data')

        bm = model.blocks(data=data)
        bm_get = model.get(bm.id)

        assert bm is not None
        assert bm_get is not None
        assert bm.id == bm_get.id

    def test_delete_blocks(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'
        info = CSVParser.load_file(path)
        data = info.get('data')

        bm = model.blocks(data=data)
        _id = bm.id
        model.delete(_id)

        assert model.get(_id) is None

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

    def test_load_lines(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/lines.csv'

        bm_1 = model.load_lines(path=path)
        bm_2 = model.load_lines(path=path)

        assert bm_1.id != bm_2.id

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

        _id = lines.id
        model.delete(_id)

        assert model.get(_id) is None

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

        _id = tubes.id
        model.delete(_id)

        assert model.get(_id) is None

    # Points
    def test_add_points(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'
        info = CSVParser.load_file(path)
        data = info.get('data')

        bm_1 = model.points(data=data)
        bm_2 = model.points(data=data)

        assert bm_1.id != bm_2.id

    def test_load_points(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'

        bm_1 = model.load_points(path=path)
        bm_2 = model.load_points(path=path)

        assert bm_1.id != bm_2.id

    def test_wrong_points(self):
        model = Model()
        with pytest.raises(Exception):
            model.load_points(f'{TEST_FILES_FOLDER_PATH}/nonexistent.csv')

    def test_get_points(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'
        info = CSVParser.load_file(path)
        data = info.get('data')

        bm = model.points(data=data)
        bm_get = model.get(bm.id)

        assert bm is not None
        assert bm_get is not None
        assert bm.id == bm_get.id

    def test_delete_points(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'
        info = CSVParser.load_file(path)
        data = info.get('data')

        bm = model.points(data=data)
        _id = bm.id
        model.delete(_id)

        assert model.get(_id) is None

    # Multiple
    def test_add_multiple(self):
        model = Model()
        elem_1 = model.load_mesh(path=f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        elem_2 = model.load_mesh(path=f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')
        elem_3 = model.load_blocks(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')

        assert elem_1.id != elem_2.id != elem_3.id

    def test_get_multiple(self):
        model = Model()
        elem_1 = model.load_mesh(path=f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        elem_2 = model.load_mesh(path=f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')
        elem_3 = model.load_blocks(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')

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
        model.load_mesh(path=f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        assert model.last_id == 0
        model.load_mesh(path=f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')
        assert model.last_id == 1
        model.load_blocks(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')
        assert model.last_id == 2

        assert model.element_collection.size() == 3

    def test_export(self):
        model = Model()
        mesh = model.load_mesh(path=f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        blocks = model.load_blocks(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')
        points = model.load_points(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')
        lines = model.load_lines(path=f'{TEST_FILES_FOLDER_PATH}/lines.csv')
        tubes = model.load_tubes(path=f'{TEST_FILES_FOLDER_PATH}/lines.csv')

        model.export(f'{TEST_FILES_FOLDER_PATH}/caseron_model_export.h5m', mesh.id)
        model.export(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_blocks.h5p', blocks.id)
        model.export(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_points.h5p', points.id)
        model.export(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_lines.csv', lines.id)
        model.export(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_tubes.csv', tubes.id)

        # Cleanup
        os.remove(f'{TEST_FILES_FOLDER_PATH}/caseron_model_export.h5m')
        os.remove(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_blocks.h5p')
        os.remove(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_points.h5p')
        os.remove(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_lines.csv')
        os.remove(f'{TEST_FILES_FOLDER_PATH}/mini_model_export_tubes.csv')
