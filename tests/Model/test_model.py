#!/usr/bin/env python

import pytest
from Model.model import Model

TEST_FILES_FOLDER_PATH = 'tests/files'


class TestModel:
    def test_add_mesh(self):
        model = Model()
        mesh_id = model.add_mesh(f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        assert mesh_id > -1

    def test_wrong_mesh(self):
        model = Model()
        mesh_id = model.add_mesh(f'{TEST_FILES_FOLDER_PATH}/nonexistent.off')
        assert mesh_id == -1

    def test_get_mesh(self):
        model = Model()
        mesh_id = model.add_mesh(f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        mesh = model.get_mesh(mesh_id)
        meshe = model.get_element(mesh_id)
        assert mesh is not None
        assert mesh == meshe

    def test_delete_mesh(self):
        model = Model()
        mesh_id = model.add_mesh(f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        element = model.get_mesh(mesh_id)
        assert element is not None

        model.delete_mesh(mesh_id)
        with pytest.raises(Exception):
            model.get_mesh(mesh_id)

    # BlockModel
    def test_add_blockmodel(self):
        model = Model()
        bm_id = model.add_block_model(f'{TEST_FILES_FOLDER_PATH}/mini.csv')
        assert bm_id > -1

    def test_wrong_blockmodel(self):
        model = Model()
        bm_id = model.add_mesh(f'{TEST_FILES_FOLDER_PATH}/nonexistent.csv')
        assert bm_id == -1

    def test_get_blockmodel(self):
        model = Model()
        bm_id = model.add_block_model(f'{TEST_FILES_FOLDER_PATH}/mini.csv')
        bm = model.get_block_model(bm_id)
        bme = model.get_block_model(bm_id)
        assert bm is not None
        assert bm == bme

    def test_delete_blockmodel(self):
        model = Model()
        bm_id = model.add_block_model(f'{TEST_FILES_FOLDER_PATH}/mini.csv')
        bm = model.get_block_model(bm_id)
        assert bm is not None

        model.delete_block_model(bm_id)
        with pytest.raises(Exception):
            model.get_block_model(bm_id)

    # Multiple
    def test_add_multiple(self):
        model = Model()
        mesh_id1 = model.add_mesh(f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        mesh_id2 = model.add_mesh(f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')
        bm_id1 = model.add_block_model(f'{TEST_FILES_FOLDER_PATH}/mini.csv')

        assert mesh_id1 != mesh_id2 != bm_id1
        mesh_1 = model.get_mesh(mesh_id1)
        mesh_2 = model.get_mesh(mesh_id2)
        bm_1 = model.get_block_model(bm_id1)
        assert mesh_1 != mesh_2 != bm_1

    def test_get_multiple(self):
        model = Model()
        mesh_id1 = model.add_mesh(f'{TEST_FILES_FOLDER_PATH}/caseron.off')
        mesh_id2 = model.add_mesh(f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')
        bm_id1 = model.add_block_model(f'{TEST_FILES_FOLDER_PATH}/mini.csv')

        m1 = model.get_mesh(mesh_id1)
        m2 = model.get_mesh(mesh_id2)
        bm = model.get_block_model(bm_id1)

        assert type(m1) == type(m2)
        assert type(m1) != type(bm)

        assert len(model.get_element_collection()) == 3
        assert len(model.get_mesh_collection()) == 2
        assert len(model.get_block_model_collection()) == 1
