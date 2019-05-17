#!/usr/bin/env python

import numpy as np
import pytest
from Model.Elements.blockmodelelement import BlockModelElement


class TestBlockModelElement:
    def test_empty_bm(self):
        with pytest.raises(Exception):
            BlockModelElement()

    def test_block_single(self):
        element = BlockModelElement(x=[-1], y=[0], z=[0])
        assert len(element.vertices) == 1

        for v in element.vertices:
            assert type(v) == np.ndarray

        expected = [[-1.0, 0.0, 0.0]]

        for i in range(len(expected)):
            for j in range(3):
                assert element.vertices[i][j] == expected[i][j]

    def test_block_multiple(self):
        element = BlockModelElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0])

        list_vertices = element.vertices
        assert len(list_vertices) == 3

        for v in list_vertices:
            assert type(v) == np.ndarray

        expected = [[-1.0, 0.0, 0.0],
                    [1.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0]]

        for i in range(len(expected)):
            for j in range(3):
                assert list_vertices[i][j] == expected[i][j]

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
        element = BlockModelElement(x=[0], y=[1], z=[2], name=name, ext=extension)
        assert element.name == name
        assert element.ext == extension

    def test_vertices_element(self):
        element = BlockModelElement(vertices=[[0, 1, 2], [3, 4, 5]])

        expected = [[0.0, 1.0, 2.0],
                    [3.0, 4.0, 5.0]]

        for i in range(len(expected)):
            for j in range(3):
                assert element.vertices[i][j] == expected[i][j]

    def test_empty_vertices(self):
        with pytest.raises(Exception):
            BlockModelElement(vertices=[])

    def test_set_vertices(self):
        element = BlockModelElement(vertices=[[0, 1, 2]])
        element.vertices = [[9, 8, 7], [6, 5, 4]]

        expected = [[9.0, 8.0, 7.0],
                    [6.0, 5.0, 4.0]]

        for i in range(len(expected)):
            for j in range(3):
                assert element.vertices[i][j] == expected[i][j]

    def test_data(self):
        data = {'x': ('0', '2', '4', '6', '8', '10'),
                'y': ('0', '0', '0', '3', '3', '1'),
                'z': ('0', '3', '3', '3', '3', '3'),
                'CuT': ('1', '0.4', '0.5', '0.8', '0.3', '0.2')}

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

        element.update_coords()
        assert element.x.size == 6
        assert element.y.size == 6
        assert element.z.size == 6
        assert len(list(element.values)) == 0

        element.update_values()
        assert element.x.size == 6
        assert element.y.size == 6
        assert element.z.size == 6
        assert len(list(element.values)) == 6

        assert element.data == data

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

        element.update_coords()
        assert element.x.size == 6
        assert element.y.size == 6
        assert element.z.size == 6

        with pytest.raises(Exception):
            element.update_values()

    def test_available_coordinates(self):
        data = {'x': ('0', '2', '4', '6', '8', '10'),
                'y': ('0', '0', '0', '3', '3', '1'),
                'z': ('0', '3', '3', '3', '3', '3'),
                'CuT': ('1', '0.4', '0.5', '0.8', '0.3', '0.2')}

        element = BlockModelElement(data=data)
        assert 'x' in list(element.available_coordinates)
        assert 'y' in list(element.available_coordinates)
        assert 'z' in list(element.available_coordinates)
        assert 'CuT' in list(element.available_coordinates)
        assert 'random' not in list(element.available_coordinates)

        element.x_str = 'x'
        element.y_str = 'y'
        element.z_str = 'z'
        element.value_str = 'CuT'

        assert 'x' in list(element.available_coordinates)
        assert 'y' in list(element.available_coordinates)
        assert 'z' in list(element.available_coordinates)
        assert 'CuT' not in list(element.available_coordinates)
        assert 'random' not in list(element.available_coordinates)

    def test_set_multiple_coordinates(self):
        data = {'x': ('0', '2', '4', '6', '8', '10'),
                'y': ('0', '0', '0', '3', '3', '1'),
                'z': ('0', '3', '3', '3', '3', '3'),
                'CuT': ('1', '0.4', '0.5', '0.8', '0.3', '0.2')}

        element = BlockModelElement(data=data)
        element.available_coordinates = ['x', 'y', 'z']
        assert 'x' in element.available_coordinates
        assert 'y' in element.available_coordinates
        assert 'z' in element.available_coordinates

    def test_available_values(self):
        data = {'x': ('0', '2', '4', '6', '8', '10'),
                'y': ('0', '0', '0', '3', '3', '1'),
                'z': ('0', '3', '3', '3', '3', '3'),
                'CuT': ('1', '0.4', '0.5', '0.8', '0.3', '0.2')}

        element = BlockModelElement(data=data)
        assert 'x' in list(element.available_values)
        assert 'y' in list(element.available_values)
        assert 'z' in list(element.available_values)
        assert 'CuT' in list(element.available_values)
        assert 'random' not in list(element.available_values)

        element.x_str = 'x'
        assert 'x' not in list(element.available_values)

        element.y_str = 'y'
        assert 'y' not in list(element.available_values)

        element.z_str = 'z'
        assert 'z' not in list(element.available_values)

        element.value_str = 'CuT'
        assert 'CuT' in list(element.available_values)
        assert 'random' not in list(element.available_values)

    def test_empty_data(self):
        with pytest.raises(Exception):
            BlockModelElement(data={})

    #
    # def test_load_ordered(self, bmelement):
    #     bmelement.load('tests/mini.csv')
    #     assert 'CuT' in bmelement.get_available_values()
    #     assert len(bmelement.get_available_coords()) == 3
    #     assert len(bmelement.get_available_values()) == 1
    #     assert bmelement.get_x_string() == 'x'
    #     assert bmelement.get_y_string() == 'y'
    #     assert bmelement.get_z_string() == 'z'
    #
    # def test_load_random(self, bmelement):
    #     bmelement.load('tests/complex.csv')
    #     assert all(elem in ['x', 'y', 'z']
    #                for elem in bmelement.get_available_coords())
    #     assert all(elem in ['ID', 'Cu', 'CuS', 'Cut', 'Mo', 'Au', 'Geol1', 'Geol2', 'Cat']
    #                for elem in bmelement.get_available_values())
    #     assert bmelement.get_x_string() == 'x'
    #     assert bmelement.get_y_string() == 'y'
    #     assert bmelement.get_z_string() == 'z'
    #
    # def test_set_strings(self, bmelement):
    #     x_str = 'easting'
    #     y_str = 'northing'
    #     z_str = 'elevation'
    #     value_str = 'CuT'
    #     bmelement.set_x_string(x_str)
    #     bmelement.set_y_string(y_str)
    #     bmelement.set_z_string(z_str)
    #     bmelement.set_value_string(value_str)
    #
    #     assert bmelement.get_x_string() == x_str
    #     assert bmelement.get_y_string() == y_str
    #     assert bmelement.get_z_string() == z_str
    #     assert bmelement.get_value_string() == value_str
    #
    # def test_get_values(self, bmelement):
    #     bmelement.load('tests/mini.csv')
    #     values_1 = bmelement.get_values()
    #
    #     bmelement.load('tests/complex.csv')
    #     values_2 = bmelement.get_values()
    #
    #     bmelement.set_value_string('Au')
    #     bmelement.update_values()
    #     values_3 = bmelement.get_values()
    #
    #     assert len(values_1) != len(values_2)
    #     assert len(values_2) == len(values_3)
    #     assert (values_2 == values_2).all()  # Of course
    #     assert not (values_2 == values_3).all()
    #
    # def test_nonstandard_headers(self, bmelement):
    #     bmelement.load('tests/mini_renamed_headers.csv')
    #     bmelement.set_x_string('easting')
    #     bmelement.set_y_string('northing')
    #     bmelement.set_z_string('elevation')
    #     bmelement.set_value_string('value')
    #
    #     assert all(elem in ['easting', 'northing', 'elevation']
    #                for elem in bmelement.get_available_coords())
    #
    #     assert all(elem in ['value']
    #                for elem in bmelement.get_available_values())
