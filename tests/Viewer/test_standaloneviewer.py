#!/usr/bin/env python

import pytest
from View.standaloneviewer import StandaloneViewer
from Model.Parsers.csvparser import CSVParser
from Model.Parsers.dxfparser import DXFParser
from Model.Parsers.offparser import OFFParser

from tests.globals import *


class TestModel:
    def test_base_viewer(self):
        viewer = StandaloneViewer()
        assert viewer
        assert viewer.model

    # def test_add_mesh(self):
    #     viewer = StandaloneViewer()
    #     path = f'{TEST_FILES_FOLDER_PATH}/caseron.dxf'
    #     vertices, indices = DXFParser.load_file(path)
    #     x, y, z = zip(*vertices)
    #
    #     mesh_1 = viewer.mesh(vertices=vertices, indices=indices, name='caseron', ext='off')
    #     mesh_2 = viewer.mesh(x=x, y=y, z=z, indices=indices, name='caseron', ext='off')
    #
    #     assert mesh_1.id != mesh_2.id
    #
    # def test_add_mesh_by_path(self):
    #     viewer = StandaloneViewer()
    #     path = f'{TEST_FILES_FOLDER_PATH}/caseron.dxf'
    #
    #     mesh_1 = viewer.mesh_by_path(path)
    #     mesh_2 = viewer.mesh_by_path(path)
    #
    #     assert mesh_1.id != mesh_2.id
    #     assert mesh_1.name == 'caseron'
    #     assert mesh_1.ext == 'dxf'
    #
    # def test_wrong_mesh(self):
    #     viewer = StandaloneViewer()
    #     with pytest.raises(Exception):
    #         viewer.mesh_by_path(f'{TEST_FILES_FOLDER_PATH}/nonexistent.off')
    #
    # def test_get_mesh(self):
    #     viewer = StandaloneViewer()
    #     path = f'{TEST_FILES_FOLDER_PATH}/caseron.off'
    #     vertices, indices = OFFParser.load_file(path)
    #
    #     mesh = viewer.mesh(vertices=vertices, indices=indices)
    #     mesh_get = viewer.get(mesh.id)
    #
    #     assert mesh is not None
    #     assert mesh_get is not None
    #     assert mesh.id == mesh_get.id
    #
    # def test_delete_mesh(self):
    #     viewer = StandaloneViewer()
    #     path = f'{TEST_FILES_FOLDER_PATH}/caseron.off'
    #     vertices, indices = OFFParser.load_file(path)
    #
    #     mesh = viewer.mesh(vertices=vertices, indices=indices)
    #     id_ = mesh.id
    #     viewer.delete(id_)
    #
    #     with pytest.raises(Exception):
    #         viewer.get(id_)
    #
    # def test_add_block_model(self):
    #     viewer = StandaloneViewer()
    #     path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'
    #     data = CSVParser.load_file(path)
    #
    #     bm_1 = viewer.block_model(data=data)
    #     bm_2 = viewer.block_model(data=data)
    #
    #     assert bm_1.id != bm_2.id
    #
    # def test_add_blockmodel_by_path(self):
    #     viewer = StandaloneViewer()
    #     path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'
    #
    #     bm_1 = viewer.block_model_by_path(path)
    #     bm_2 = viewer.block_model_by_path(path)
    #
    #     assert bm_1.id != bm_2.id
    #
    # def test_wrong_blockmodel(self):
    #     viewer = StandaloneViewer()
    #     with pytest.raises(Exception):
    #         viewer.block_model_by_path(f'{TEST_FILES_FOLDER_PATH}/nonexistent.csv')
    #
    # def test_get_blockmodel(self):
    #     viewer = StandaloneViewer()
    #     path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'
    #     data = CSVParser.load_file(path)
    #
    #     bm = viewer.block_model(data=data)
    #     bm_get = viewer.get(bm.id)
    #
    #     assert bm is not None
    #     assert bm_get is not None
    #     assert bm.id == bm_get.id
    #
    # def test_delete_blockmodel(self):
    #     viewer = StandaloneViewer()
    #     path = f'{TEST_FILES_FOLDER_PATH}/mini.csv'
    #     data = CSVParser.load_file(path)
    #
    #     bm = viewer.block_model(data=data)
    #     id_ = bm.id
    #     viewer.delete(id_)
    #
    #     with pytest.raises(Exception):
    #         viewer.get(id_)
    #
    # # Multiple
    # def test_add_multiple(self):
    #     viewer = StandaloneViewer()
    #     elem_1 = viewer.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.off')
    #     elem_2 = viewer.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')
    #     elem_3 = viewer.block_model_by_path(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')
    #
    #     assert elem_1.id != elem_2.id != elem_3.id
    #
    # def test_get_multiple(self):
    #     viewer = StandaloneViewer()
    #     elem_1 = viewer.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.off')
    #     elem_2 = viewer.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')
    #     elem_3 = viewer.block_model_by_path(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')
    #
    #     assert type(elem_1) == type(elem_2)
    #     assert type(elem_2) != type(elem_3)
    #
    #     elem_get_1 = viewer.get(elem_1.id)
    #     elem_get_2 = viewer.get(elem_2.id)
    #     elem_get_3 = viewer.get(elem_3.id)
    #
    #     assert type(elem_get_1) == type(elem_get_2)
    #     assert type(elem_get_2) != type(elem_get_3)
    #
    # def test_collection_types(self):
    #     viewer = StandaloneViewer()
    #     viewer.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.off')
    #     viewer.mesh_by_path(path=f'{TEST_FILES_FOLDER_PATH}/caseron.dxf')
    #     viewer.block_model_by_path(path=f'{TEST_FILES_FOLDER_PATH}/mini.csv')
    #
    #     assert len(viewer.element_collection) == 3
    #     assert len(viewer.mesh_collection) == 2
    #     assert len(viewer.block_model_collection) == 1
