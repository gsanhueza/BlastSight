#!/usr/bin/env python

import numpy as np
import pytest
from blastsight.model.elements.pointelement import PointElement


class TestPointElement:
    def test_empty_point(self):
        with pytest.raises(Exception):
            PointElement()

    def test_point_single(self):
        element = PointElement(x=[-1], y=[0], z=[0], values=[0])
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

    def test_point_multiple(self):
        element = PointElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[10, 20, 30])

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

    def test_wrong_point(self):
        with pytest.raises(Exception):
            PointElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0])

        with pytest.raises(Exception):
            PointElement(x=[-1, 1, 0], y=[0, 0], z=[0, 0, 0])

        with pytest.raises(Exception):
            PointElement(x=[-1, 1], y=[0, 0], z=[0, 0, 1])

    def test_named_element(self):
        name = "NAME"
        extension = "EXT"
        element = PointElement(x=[0], y=[1], z=[2], values=[0], name=name, extension=extension)
        assert element.name == name
        assert element.extension == extension

    def test_vertices_element(self):
        element = PointElement(vertices=[[0, 1, 2], [3, 4, 5]], values=[0, 0])

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
            PointElement(vertices=[])

    def test_data(self):
        data = {'x': [0.0, 2.0, 4.0, 6.0, 8.0, 10.0],
                'y': [0.0, 0.0, 0.0, 3.0, 3.0, 1.0],
                'z': [0.0, 3.0, 3.0, 3.0, 3.0, 3.0],
                'CuT': [1.0, 0.4, 0.5, 0.8, 0.3, 0.2],
                }

        element = PointElement(data=data)
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
        data = {'x': ['0', '2', '4', '6', '8', '10'],
                'y': ['0', '0', '0', '3', '3', '1'],
                'z': ['0', '3', '3', '3', '3', '3']}

        with pytest.raises(Exception):
            PointElement(data)

    def test_inconsistent_data(self):
        data = {'x': ['0', '2', '4', '6', '8', '10'],
                'y': ['0', '0', '0', '3', '3', '1'],
                'z': ['0', '3', '3', '3', '3'],
                'CuT': ['1', '0.4', '0.5', '0.8', '0.3', '0.2']}

        with pytest.raises(Exception):
            PointElement(data)

        data = {'x': ['0', '2', '4', '6', '8', '10'],
                'y': ['0', '0', '0', '3', '3', '1'],
                'z': ['0', '3', '3', '3', '3', '3'],
                'CuT': ['1', '0.4', '0.5', '0.8', '0.3']}

        with pytest.raises(Exception):
            PointElement(data)

        data = {'x': ['0', '2', '4', '6', '8'],
                'y': ['0', '0', '0', '3', '3'],
                'z': ['0', '3', '3', '3', '3'],
                'CuT': ['1', '0.4', '0.5', '0.8', '0.3', '0.2']}

        with pytest.raises(Exception):
            PointElement(data)

    def test_alter_headers(self):
        data = {'x': [0.0, 2.0, 4.0, 6.0, 8.0, 10.0],
                'y': [0.0, 0.0, 0.0, 3.0, 3.0, 1.0],
                'z': [0.0, 3.0, 3.0, 3.0, 3.0, 3.0],
                'CuT': [1.0, 0.4, 0.5, 0.8, 0.3, 0.2]}

        element = PointElement(data=data)
        element.headers = ['x', 'y', 'z', 'value']
        expected = ['x', 'y', 'z', 'value']

        for e, r in zip(expected, element.headers):
            assert e == r

    def test_available_coordinates(self):
        data = {'easting': ['0', '2', '4', '6', '8', '10'],
                'northing': ['0', '0', '0', '3', '3', '1'],
                'elevation': ['0', '3', '3', '3', '3', '3'],
                'CuT': ['1', '0.4', '0.5', '0.8', '0.3', '0.2']}

        element = PointElement(data=data)
        assert 'easting' in list(element.headers)
        assert 'northing' in list(element.headers)
        assert 'elevation' in list(element.headers)
        assert 'CuT' in list(element.headers)
        assert 'random' not in list(element.headers)

    def test_set_multiple_coordinates(self):
        data = {'x': ['0', '2', '4', '6', '8', '10'],
                'y': ['0', '0', '0', '3', '3', '1'],
                'z': ['0', '3', '3', '3', '3', '3'],
                'CuT': ['1', '0.4', '0.5', '0.8', '0.3', '0.2']}

        element = PointElement(data=data)
        element.headers = ['x', 'y', 'z', 'CuT']
        assert 'x' in element.headers
        assert 'y' in element.headers
        assert 'z' in element.headers
        assert 'CuT' in element.headers

    def test_empty_data(self):
        with pytest.raises(Exception):
            PointElement(data={})

    def test_point_size(self):
        element = PointElement(vertices=[[0, 1, 2], [3, 4, 5]], values=[8, 16], point_size=[2.0, 4.0])
        assert element.point_size[0] == 2.0
        assert element.point_size[1] == 4.0
        assert element.avg_size == 3.0

        element.avg_size = 5.0
        assert element.point_size[0] == 5.0
        assert element.point_size[1] == 5.0

        element.point_size = 10.0
        assert element.point_size[0] == 10.0
        assert element.point_size[1] == 10.0
        assert element.avg_size == 10.0

    def test_markers(self):
        element = PointElement(vertices=[[0, 1, 2]], values=[8])
        assert element.marker == 'square'
        assert element.marker_num == element.marker_dict.get('square')

        element.marker = 'sphere'
        assert element.marker == 'sphere'
        assert element.marker_num == element.marker_dict.get('sphere')
