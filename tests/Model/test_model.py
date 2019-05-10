#!/usr/bin/env python

import pytest
from Model.model import Model


class TestModel:
    def test_init(self):
        model = Model()
        assert model is not None

    def test_add_mesh(self):
        model = Model()
        mesh_id = model.add_mesh('tests/caseron.off')
        assert mesh_id > -1

    def test_get_mesh(self):
        model = Model()
        mesh_id = model.add_mesh('tests/caseron.off')
        mesh = model.get_element(mesh_id)
        assert mesh is not None

    def test_update_mesh(self):
        model = Model()
        mesh_id = model.add_mesh('tests/caseron.off')
        mesh_1 = model.get_element(mesh_id)
        model.update_mesh(mesh_id, 'tests/caseron.off')
        mesh_2 = model.get_element(mesh_id)
        assert mesh_1.get_vertices().all() == mesh_2.get_vertices().all()
        assert mesh_1.get_indices().all() == mesh_2.get_indices().all()
        assert mesh_1.get_values().all() == mesh_2.get_values().all()
        assert mesh_1.get_centroid().all() == mesh_2.get_centroid().all()

    def test_delete_mesh(self):
        model = Model()
        mesh_id = model.add_mesh('tests/caseron.off')
        element = model.get_element(mesh_id)
        assert element is not None

        model.delete_mesh(mesh_id)
        with pytest.raises(Exception):
            model.get_element(mesh_id)

    def test_add_multiple(self):
        model = Model()
        mesh_id1 = model.add_mesh('tests/caseron.off')
        mesh_id2 = model.add_mesh('tests/caseron.dxf')

        assert mesh_id1 != mesh_id2
        mesh_1 = model.get_mesh(mesh_id1)
        mesh_2 = model.get_mesh(mesh_id2)
        assert mesh_1 != mesh_2

    def test_get_multiple(self):
        model = Model()
        mesh_id = model.add_mesh('tests/caseron.off')

        assert type(model.get_element_collection()) is list
        assert type(model.get_element_collection()[0]) is tuple
        assert model.get_element_collection()[0][0] == mesh_id
