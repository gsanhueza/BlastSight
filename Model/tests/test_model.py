#!/usr/bin/env python

import pytest
from Model.Parsers.offparser import OFFParser
from Model.Parsers.csvparser import CSVParser
from Model.model import Model
from Model.tests.globals import *


class TestModel:
    # Mesh
    def test_add_mesh(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/caseron.off'
        vertices, indices = OFFParser.load_file(path)
        x, y, z = zip(*vertices)

        mesh_1 = model.mesh(vertices=vertices, indices=indices, name='caseron', ext='off')
        mesh_2 = model.mesh(x=x, y=y, z=z, indices=indices, name='caseron', ext='off')

        assert mesh_1.id != mesh_2.id

    def test_add_mesh_by_path(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/caseron.dxf'

        mesh_1 = model.mesh_by_path(path=path)
        mesh_2 = model.mesh_by_path(path=path)

        assert mesh_1.id != mesh_2.id
        assert mesh_1.name == 'caseron'
        assert mesh_1.ext == 'dxf'

    def test_wrong_mesh(self):
        model = Model()
        with pytest.raises(Exception):
            model.mesh_by_path(f'{TEST_FILES_FOLDER_PATH}/nonexistent.off')

    def test_get_mesh(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/caseron.off'
        vertices, indices = OFFParser.load_file(path)

        mesh = model.mesh(vertices=vertices, indices=indices)
        mesh_get = model.get(mesh.id)

        assert mesh is not None
        assert mesh_get is not None
        assert mesh.id == mesh_get.id

    def test_delete_mesh(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/caseron.off'
        vertices, indices = OFFParser.load_file(path)

        mesh = model.mesh(vertices=vertices, indices=indices)
        id_ = mesh.id
        model.delete(id_)

        with pytest.raises(Exception):
            model.get(id_)

    # Block model
    def test_add_block_model(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'
        data = CSVParser.load_file(path)

        bm_1 = model.block_model(data=data)
        bm_2 = model.block_model(data=data)

        assert bm_1.id != bm_2.id

    def test_add_blockmodel_by_path(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'

        bm_1 = model.block_model_by_path(path=path)
        bm_2 = model.block_model_by_path(path=path)

        assert bm_1.id != bm_2.id

    def test_wrong_blockmodel(self):
        model = Model()
        with pytest.raises(Exception):
            model.block_model_by_path(f'{TEST_FILES_FOLDER_PATH}/nonexistent.csv')

    def test_get_blockmodel(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'
        data = CSVParser.load_file(path)

        bm = model.block_model(data=data)
        bm_get = model.get(bm.id)

        assert bm is not None
        assert bm_get is not None
        assert bm.id == bm_get.id

    def test_delete_blockmodel(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'
        data = CSVParser.load_file(path)

        bm = model.block_model(data=data)
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

    # Multiple
    def test_add_multiple(self):
        model = Model()
        elem_1 = model.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        elem_2 = model.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')
        elem_3 = model.block_model_by_path(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')

        assert elem_1.id != elem_2.id != elem_3.id

    def test_get_multiple(self):
        model = Model()
        elem_1 = model.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        elem_2 = model.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')
        elem_3 = model.block_model_by_path(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')

        assert type(elem_1) == type(elem_2)
        assert type(elem_2) != type(elem_3)

        elem_get_1 = model.get(elem_1.id)
        elem_get_2 = model.get(elem_2.id)
        elem_get_3 = model.get(elem_3.id)

        assert type(elem_get_1) == type(elem_get_2)
        assert type(elem_get_2) != type(elem_get_3)

    def test_collection_types(self):
        model = Model()
        model.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        model.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')
        model.block_model_by_path(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')

        assert len(model.element_collection) == 3
        assert len(model.mesh_collection) == 2
        assert len(model.block_model_collection) == 1
