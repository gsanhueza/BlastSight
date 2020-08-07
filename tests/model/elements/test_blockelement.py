#!/usr/bin/env python

import numpy as np
import pytest
from blastsight.model.elements.blockelement import BlockElement


class TestBlockElement:
    def test_empty_bm(self):
        with pytest.raises(Exception):
            BlockElement()

    def test_block_single(self):
        element = BlockElement(x=[-1], y=[0], z=[0], values=[0])
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
        element = BlockElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[10, 20, 30])

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
            BlockElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0])

        with pytest.raises(Exception):
            BlockElement(x=[-1, 1, 0], y=[0, 0], z=[0, 0, 0])

        with pytest.raises(Exception):
            BlockElement(x=[-1, 1], y=[0, 0], z=[0, 0, 1])

    def test_named_element(self):
        name = "NAME"
        extension = "EXT"
        element = BlockElement(x=[0], y=[1], z=[2], values=[0], name=name, extension=extension)
        assert element.name == name
        assert element.extension == extension

    def test_vertices_element(self):
        element = BlockElement(vertices=[[0, 1, 2], [3, 4, 5]], values=[0, 0])

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
            BlockElement(vertices=[])

    def test_data(self):
        data = {'x': [0.0, 2.0, 4.0, 6.0, 8.0, 10.0],
                'y': [0.0, 0.0, 0.0, 3.0, 3.0, 1.0],
                'z': [0.0, 3.0, 3.0, 3.0, 3.0, 3.0],
                'CuT': [1.0, 0.4, 0.5, 0.8, 0.3, 0.2],
                }

        element = BlockElement(data=data)
        expected = list(data.keys())

        for e, r in zip(expected, element.headers):
            assert e == r

        assert element.x.size == 6
        assert element.y.size == 6
        assert element.z.size == 6
        assert len(list(element.values)) == 6

        epsilon = 0.0001
        for key in data.keys():
            for ed, d in zip(element.data[key].tolist(), data[key]):
                assert abs(ed - d) < epsilon

    def test_insufficient_data(self):
        data = {'x': [0.0, 2.0, 4.0, 6.0, 8.0, 10.0],
                'y': [0.0, 0.0, 0.0, 3.0, 3.0, 1.0],
                'z': [0.0, 3.0, 3.0, 3.0, 3.0, 3.0]}

        with pytest.raises(Exception):
            BlockElement(data)

    def test_inconsistent_data(self):
        data = {'x': [0.0, 2.0, 4.0, 6.0, 8.0, 10.0],
                'y': [0.0, 0.0, 0.0, 3.0, 3.0, 1.0],
                'z': [0.0, 3.0, 3.0, 3.0, 3.0],
                'CuT': [1.0, 0.4, 0.5, 0.8, 0.3, 0.2]}

        with pytest.raises(Exception):
            BlockElement(data)

        data = {'x': [0.0, 2.0, 4.0, 6.0, 8.0, 10.0],
                'y': [0.0, 0.0, 0.0, 3.0, 3.0, 1.0],
                'z': [0.0, 3.0, 3.0, 3.0, 3.0, 3.0],
                'CuT': [1.0, 0.4, 0.5, 0.8, 0.3]}

        with pytest.raises(Exception):
            BlockElement(data)

        data = {'x': [0.0, 2.0, 4.0, 6.0, 8.0],
                'y': ['0', '0', '0', '3', '3'],
                'z': [0.0, 3.0, 3.0, 3.0, 3.0],
                'CuT': [1.0, 0.4, 0.5, 0.8, 0.3, 0.2]}

        with pytest.raises(Exception):
            BlockElement(data)

    def test_alter_headers(self):
        data = {'x': [0.0, 2.0, 4.0, 6.0, 8.0, 10.0],
                'y': [0.0, 0.0, 0.0, 3.0, 3.0, 1.0],
                'z': [0.0, 3.0, 3.0, 3.0, 3.0, 3.0],
                'CuT': [1.0, 0.4, 0.5, 0.8, 0.3, 0.2]}

        element = BlockElement(data=data)
        element.headers = ['x', 'y', 'z', 'value']
        expected = ['x', 'y', 'z', 'value']

        for e, r in zip(expected, element.headers):
            assert e == r

    def test_available_coordinates(self):
        data = {'easting': [0.0, 2.0, 4.0, 6.0, 8.0, 10.0],
                'northing': [0.0, 0.0, 0.0, 3.0, 3.0, 1.0],
                'elevation': [0.0, 3.0, 3.0, 3.0, 3.0, 3.0],
                'CuT': [1.0, 0.4, 0.5, 0.8, 0.3, 0.2]}

        element = BlockElement(data=data)
        assert 'easting' in list(element.headers)
        assert 'northing' in list(element.headers)
        assert 'elevation' in list(element.headers)
        assert 'CuT' in list(element.headers)
        assert 'random' not in list(element.headers)

    def test_set_multiple_coordinates(self):
        data = {'x': [0.0, 2.0, 4.0, 6.0, 8.0, 10.0],
                'y': [0.0, 0.0, 0.0, 3.0, 3.0, 1.0],
                'z': [0.0, 3.0, 3.0, 3.0, 3.0, 3.0],
                'CuT': [1.0, 0.4, 0.5, 0.8, 0.3, 0.2]}

        element = BlockElement(data=data)
        element.headers = ['x', 'y', 'z', 'CuT']
        assert 'x' in element.headers
        assert 'y' in element.headers
        assert 'z' in element.headers
        assert 'CuT' in element.headers

    def test_empty_data(self):
        with pytest.raises(Exception):
            BlockElement(data={})

    def test_block_size(self):
        element = BlockElement(vertices=[[0, 1, 2]], values=[8], block_size=[2.0, 4.0, 7.0])
        epsilon = 0.0001

        assert abs(element.block_size[0] - 2.0) < epsilon
        assert abs(element.block_size[1] - 4.0) < epsilon
        assert abs(element.block_size[2] - 7.0) < epsilon

        element.block_size = [2.3, 4.2, 7.1]
        assert abs(element.block_size[0] - 2.3) < epsilon
        assert abs(element.block_size[1] - 4.2) < epsilon
        assert abs(element.block_size[2] - 7.1) < epsilon

    def test_auto_size(self):
        data = {'x': [0.0, 2.0, 4.0, 6.0, 8.0, 10.0],
                'y': [0.0, 0.0, 0.0, 3.0, 3.0, 1.0],
                'z': [0.0, 3.0, 3.0, 3.0, 3.0, 3.0],
                'CuT': [1.0, 0.4, 0.5, 0.8, 0.3, 0.2]}

        element = BlockElement(data=data, autosize=False)
        assert element.block_size[0] == 1.0
        assert element.block_size[1] == 1.0
        assert element.block_size[2] == 1.0

        expected = [2.0, 2.0, 3.0]
        for i, j in zip(element.get_autosize(), expected):
            assert i == j

        element = BlockElement(data=data, autosize=True)
        assert element.block_size[0] == 2.0
        assert element.block_size[1] == 2.0
        assert element.block_size[2] == 3.0

    def test_bounding_box(self):
        element = BlockElement(vertices=[[0, 0, 0]], values=[0])

        expected_lo = [-0.5, -0.5, -0.5]
        expected_hi = [0.5, 0.5, 0.5]

        for i, j in zip(expected_lo, expected_hi):
            for k in range(len(expected_lo)):
                assert i == element.bounding_box[0][k]
                assert j == element.bounding_box[1][k]
