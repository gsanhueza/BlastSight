#!/usr/bin/env python

import numpy as np
import pytest
from libraries.Model.Elements.blockmodelelement import BlockModelElement


class TestBlockModelElement:
    def test_empty_bm(self):
        with pytest.raises(Exception):
            BlockModelElement()

    def test_block_single(self):
        element = BlockModelElement(x=[-1], y=[0], z=[0], values=[0])
        assert len(element.vertices) == 1

        for v in element.vertices:
            assert type(v) == np.ndarray

        # Coordinates
        expected = [[-1.0, 0.0, 0.0]]

        for i in range(len(expected)):
            for j in range(3):
                assert element.vertices[i][j] == expected[i][j]

        # Values
        expected = [0]
        assert element.values.size == len(expected)
        for i in range(len(expected)):
            assert element.values[i] == expected[i]

    def test_block_multiple(self):
        element = BlockModelElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[10, 20, 30])

        list_vertices = element.vertices
        assert len(list_vertices) == 3

        for v in list_vertices:
            assert type(v) == np.ndarray

        # Coordinates
        expected = [[-1.0, 0.0, 0.0],
                    [1.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0]]

        for i in range(len(expected)):
            for j in range(3):
                assert list_vertices[i][j] == expected[i][j]

        # Values
        expected = [10, 20, 30]
        assert element.values.size == len(expected)
        for i in range(len(expected)):
            assert element.values[i] == expected[i]

    def test_wrong_bm(self):
        with pytest.raises(Exception):
            BlockModelElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0])

        with pytest.raises(Exception):
            BlockModelElement(x=[-1, 1, 0], y=[0, 0], z=[0, 0, 0])

        with pytest.raises(Exception):
            BlockModelElement(x=[-1, 1], y=[0, 0], z=[0, 0, 1])

    def test_named_element(self):
        name = "NAME"
        extension = "EXT"
        element = BlockModelElement(x=[0], y=[1], z=[2], values=[0], name=name, ext=extension)
        assert element.name == name
        assert element.ext == extension

    def test_vertices_element(self):
        element = BlockModelElement(vertices=[[0, 1, 2], [3, 4, 5]], values=[0, 0])

        # Coordinates
        expected = [[0.0, 1.0, 2.0],
                    [3.0, 4.0, 5.0]]

        for i in range(len(expected)):
            for j in range(3):
                assert element.vertices[i][j] == expected[i][j]

        # Values
        expected = [0, 0]
        assert element.values.size == len(expected)
        for i in range(len(expected)):
            assert element.values[i] == expected[i]

    def test_empty_vertices(self):
        with pytest.raises(Exception):
            BlockModelElement(vertices=[])

    def test_set_vertices(self):
        element = BlockModelElement(vertices=[[0, 1, 2]], values=[8])
        element.vertices = [[9, 8, 7], [6, 5, 4]]

        # Coordinates
        expected = [[9.0, 8.0, 7.0],
                    [6.0, 5.0, 4.0]]

        for i in range(len(expected)):
            for j in range(3):
                assert element.vertices[i][j] == expected[i][j]

        # Values
        expected = [8]
        assert element.values.size == len(expected)
        for i in range(len(expected)):
            assert element.values[i] == expected[i]

    def test_data(self):
        data = {'x': [0.0, 2.0, 4.0, 6.0, 8.0, 10.0],
                'y': [0.0, 0.0, 0.0, 3.0, 3.0, 1.0],
                'z': [0.0, 3.0, 3.0, 3.0, 3.0, 3.0],
                'CuT': [1.0, 0.4, 0.5, 0.8, 0.3, 0.2],
                }

        element = BlockModelElement(data=data)
        element.x_str = 'x'
        element.y_str = 'y'
        element.z_str = 'z'
        element.value_str = 'CuT'

        assert element.x.size == 0
        assert element.y.size == 0
        assert element.z.size == 0
        assert element.values.size == 0

        assert element.x_str == 'x'
        assert element.y_str == 'y'
        assert element.z_str == 'z'
        assert element.value_str == 'CuT'

        element.update_values()
        assert element.x.size == 6
        assert element.y.size == 6
        assert element.z.size == 6
        assert len(list(element.values)) == 6

        epsilon = 0.0001
        for key in data.keys():
            for ed, d in zip(element.data[key].tolist(), data[key]):
                assert abs(ed - d) < epsilon

    def test_insufficient_data(self):
        data = {'x': ('0', '2', '4', '6', '8', '10'),
                'y': ('0', '0', '0', '3', '3', '1'),
                'z': ('0', '3', '3', '3', '3', '3')}

        with pytest.raises(Exception):
            BlockModelElement(data)

    def test_inconsistent_data(self):
        data = {'x': ('0', '2', '4', '6', '8', '10'),
                'y': ('0', '0', '0', '3', '3', '1'),
                'z': ('0', '3', '3', '3', '3'),
                'CuT': ('1', '0.4', '0.5', '0.8', '0.3', '0.2')}

        with pytest.raises(Exception):
            BlockModelElement(data)

        data = {'x': ('0', '2', '4', '6', '8', '10'),
                'y': ('0', '0', '0', '3', '3', '1'),
                'z': ('0', '3', '3', '3', '3', '3'),
                'CuT': ('1', '0.4', '0.5', '0.8', '0.3')}

        with pytest.raises(Exception):
            BlockModelElement(data)

        data = {'x': ('0', '2', '4', '6', '8'),
                'y': ('0', '0', '0', '3', '3'),
                'z': ('0', '3', '3', '3', '3'),
                'CuT': ('1', '0.4', '0.5', '0.8', '0.3', '0.2')}

        with pytest.raises(Exception):
            BlockModelElement(data)

    def test_data_wrong_string(self):
        data = {'x': ('0', '2', '4', '6', '8', '10'),
                'y': ('0', '0', '0', '3', '3', '1'),
                'z': ('0', '3', '3', '3', '3', '3'),
                'CuT': ('1', '0.4', '0.5', '0.8', '0.3', '0.2')}

        element = BlockModelElement(data=data)
        element.x_str = 'x'
        element.y_str = 'y'
        element.z_str = 'z'
        element.value_str = 'value'

        assert element.x_str == 'x'
        assert element.y_str == 'y'
        assert element.z_str == 'z'
        assert element.value_str == 'value'

        with pytest.raises(Exception):
            element.update_values()

    def test_available_coordinates(self):
        data = {'easting': ('0', '2', '4', '6', '8', '10'),
                'northing': ('0', '0', '0', '3', '3', '1'),
                'elevation': ('0', '3', '3', '3', '3', '3'),
                'CuT': ('1', '0.4', '0.5', '0.8', '0.3', '0.2')}

        element = BlockModelElement(data=data)
        assert 'easting' in list(element.available_headers)
        assert 'northing' in list(element.available_headers)
        assert 'elevation' in list(element.available_headers)
        assert 'CuT' in list(element.available_headers)
        assert 'random' not in list(element.available_headers)

    def test_set_multiple_coordinates(self):
        data = {'x': ('0', '2', '4', '6', '8', '10'),
                'y': ('0', '0', '0', '3', '3', '1'),
                'z': ('0', '3', '3', '3', '3', '3'),
                'CuT': ('1', '0.4', '0.5', '0.8', '0.3', '0.2')}

        element = BlockModelElement(data=data)
        element.available_headers = ['x', 'y', 'z', 'CuT']
        assert 'x' in element.available_headers
        assert 'y' in element.available_headers
        assert 'z' in element.available_headers
        assert 'CuT' in element.available_headers

    def test_empty_data(self):
        with pytest.raises(Exception):
            BlockModelElement(data={})

    def test_block_size(self):
        element = BlockModelElement(vertices=[[0, 1, 2]], values=[8], block_size=[2.0, 4.0, 7.0])
        epsilon = 0.0001

        assert abs(element.block_size[0] - 2.0) < epsilon
        assert abs(element.block_size[1] - 4.0) < epsilon
        assert abs(element.block_size[2] - 7.0) < epsilon

        element.block_size = [2.3, 4.2, 7.1]
        assert abs(element.block_size[0] - 2.3) < epsilon
        assert abs(element.block_size[1] - 4.2) < epsilon
        assert abs(element.block_size[2] - 7.1) < epsilon
