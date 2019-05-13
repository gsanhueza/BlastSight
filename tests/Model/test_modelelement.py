#!/usr/bin/env python

import pytest
import numpy as np
from Model.modelelement import ModelElement
from Model.Mesh.meshelement import MeshElement
from Model.BlockModel.blockmodelelement import BlockModelElement


@pytest.fixture(scope='class', autouse=True)
def element():
    return ModelElement()


@pytest.fixture(scope='class', autouse=True)
def meshelement():
    return MeshElement()


@pytest.fixture(scope='class', autouse=True)
def bmelement():
    return BlockModelElement()


class TestModelElement:
    def test_empty_mesh(self, element):
        assert type(element.get_vertices()) is np.ndarray
        assert type(element.get_indices()) is np.ndarray
        assert type(element.get_values()) is np.ndarray
        assert type(element.get_centroid()) is np.ndarray

    def test_set_vertices(self, element):
        data = [[0.0, 1.0, 2.0]]
        element.set_vertices(data)

        element_data = element.get_vertices()

        for i in range(len(data)):
            assert all(element_data[i]) == all(data[i])

    def test_set_indices(self, element):
        data = [0, 1, 2]
        element.set_indices(data)

        element_data = element.get_indices()

        for i in range(len(data)):
            assert element_data[i] == data[i]

    def test_set_values(self, element):
        data = [0.0, 1.0, 2.0]
        element.set_values(data)

        element_data = element.get_values()

        for i in range(len(data)):
            assert element_data[i] == data[i]


class TestMeshElement(TestModelElement):
    pass


class TestBlockModelElement(TestModelElement):
    def test_load_ordered(self, bmelement):
        bmelement.load('tests/mini.csv')
        assert 'CuT' in bmelement.get_available_values()
        assert len(bmelement.get_available_values()) == 1
        assert bmelement.get_x_string() == 'x'
        assert bmelement.get_y_string() == 'y'
        assert bmelement.get_z_string() == 'z'

    def test_load_random(self, bmelement):
        bmelement.load('tests/complex.csv')
        assert all(elem in ['ID', 'Cu', 'CuS', 'Cut', 'Mo', 'Au', 'Geol1', 'Geol2', 'Cat']
                   for elem in bmelement.get_available_values())
        assert bmelement.get_x_string() == 'x'
        assert bmelement.get_y_string() == 'y'
        assert bmelement.get_z_string() == 'z'

    def test_set_strings(self, bmelement):
        x_str = 'easting'
        y_str = 'northing'
        z_str = 'elevation'
        value_str = 'CuT'
        bmelement.set_x_string(x_str)
        bmelement.set_y_string(y_str)
        bmelement.set_z_string(z_str)
        bmelement.set_value_string(value_str)

        assert bmelement.get_x_string() == x_str
        assert bmelement.get_y_string() == y_str
        assert bmelement.get_z_string() == z_str
        assert bmelement.get_value_string() == value_str
