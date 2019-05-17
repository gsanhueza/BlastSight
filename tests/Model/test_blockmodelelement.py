#!/usr/bin/env python

import numpy as np
import pytest
from Model.BlockModel.blockmodelelement import BlockModelElement


class TestBlockModelElement:
    def test_empty_bm(self):
        with pytest.raises(Exception):
            BlockModelElement()

    def test_block_single(self):
        element = BlockModelElement(x=[-1], y=[0], z=[0])

        list_vertices = element.vertices
        assert len(list_vertices) == 1

        for v in list_vertices:
            assert type(v) == np.ndarray

        assert all(list_vertices[0]) == all([-1.0, 0.0, 0.0])

    def test_block_multiple(self):
        element = BlockModelElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0])

        list_vertices = element.vertices
        assert len(list_vertices) == 3

        for v in list_vertices:
            assert type(v) == np.ndarray

        assert all(list_vertices[0].tolist()) == all([-1.0, 0.0, 0.0])
        assert all(list_vertices[1].tolist()) == all([1.0, 0.0, 0.0])
        assert all(list_vertices[2].tolist()) == all([0.0, 1.0, 0.0])

    def test_wrong_bm(self):
        with pytest.raises(Exception):
            BlockModelElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0])

        with pytest.raises(Exception):
            BlockModelElement(x=[-1, 1, 0], y=[0, 0], z=[0, 0, 0])

        with pytest.raises(Exception):
            BlockModelElement(x=[-1, 1], y=[0, 0], z=[0, 0, 1])

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
