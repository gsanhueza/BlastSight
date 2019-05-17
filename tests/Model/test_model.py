#!/usr/bin/env python

import pytest
from Model.Parsers.offparser import OFFParser
from Model.Parsers.csvparser import CSVParser
from Model.model import Model

TEST_FILES_FOLDER_PATH = 'tests/files'


class TestModel:
    def test_add_mesh(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/caseron.off'
        vertices, indices = OFFParser.load_file(path)

        mesh_1, id_1 = model.mesh(vertices=vertices, indices=indices)
        mesh_2, id_2 = model.mesh(vertices=vertices, indices=indices)

        assert mesh_1.id == id_1 == 0
        assert mesh_2.id == id_2 == 1

    def test_add_mesh_by_path(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/caseron.dxf'

        mesh_1, id_1 = model.mesh_by_path(path=path)
        mesh_2, id_2 = model.mesh_by_path(path=path)

        assert mesh_1.id == id_1 == 0
        assert mesh_2.id == id_2 == 1

    def test_wrong_mesh(self):
        model = Model()
        with pytest.raises(Exception):
            model.mesh_by_path(f'{TEST_FILES_FOLDER_PATH}/nonexistent.off')

    def test_get_mesh(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/caseron.off'
        vertices, indices = OFFParser.load_file(path)

        mesh, id_ = model.mesh(vertices=vertices, indices=indices)
        mesh_get = model.get(id_)

        assert mesh is not None
        assert mesh_get is not None
        assert mesh.id == mesh_get.id

    def test_delete_mesh(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/caseron.off'
        vertices, indices = OFFParser.load_file(path)

        _, id_ = model.mesh(vertices=vertices, indices=indices)

        model.delete_mesh(id_)
        with pytest.raises(Exception):
            model.get(id_)

    def test_add_blockmodel(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'
        data = CSVParser.load_file(path)

        bm_1, id_1 = model.blockmodel(data=data)
        bm_2, id_2 = model.blockmodel(data=data)

        assert bm_1.id == id_1 == 0
        assert bm_2.id == id_2 == 1

    def test_add_blockmodel_by_path(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'

        bm_1, id_1 = model.blockmodel_by_path(path=path)
        bm_2, id_2 = model.blockmodel_by_path(path=path)

        assert bm_1.id == id_1 == 0
        assert bm_2.id == id_2 == 1

    def test_wrong_blockmodel(self):
        model = Model()
        with pytest.raises(Exception):
            model.blockmodel_by_path(f'{TEST_FILES_FOLDER_PATH}/nonexistent.csv')

    def test_get_blockmodel(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/caseron.off'
        data = CSVParser.load_file(path)

        bm, id_ = model.mesh(data=data)
        bm_get = model.get(id_)

        assert bm is not None
        assert bm_get is not None
        assert bm.id == bm_get.id

    def test_delete_blockmodel(self):
        model = Model()
        path = f'{TEST_FILES_FOLDER_PATH}/caseron.off'
        vertices, indices = OFFParser.load_file(path)

        _, id_ = model.blockmodel(vertices=vertices, indices=indices)

        model.delete_blockmodel(id_)
        with pytest.raises(Exception):
            model.get(id_)

    # FIXME Recreate tests from here

    # Multiple
    def test_add_multiple(self):
        model = Model()
        elem_1, id_1 = model.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        elem_2, id_2 = model.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')
        elem_3, id_3 = model.blockmodel_by_path(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')

        assert id_1 != id_2 != id_3
        assert elem_1 == id_1
        assert elem_2 == id_2
        assert elem_3 == id_3

    def test_get_multiple(self):
        model = Model()
        elem_1, id_1 = model.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        elem_2, id_2 = model.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')
        elem_3, id_3 = model.blockmodel_by_path(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')

        assert type(elem_1) == type(elem_2)
        assert type(elem_2) != type(elem_3)

        elem_get_1 = model.get(id_1)
        elem_get_2 = model.get(id_2)
        elem_get_3 = model.get(id_3)

        assert type(elem_get_1) == type(elem_get_2)
        assert type(elem_get_2) != type(elem_get_3)

        assert len(model.get_element_collection()) == 3
        assert len(model.get_mesh_collection()) == 2
        assert len(model.get_block_model_collection()) == 1
