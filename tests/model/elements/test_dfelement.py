#!/usr/bin/env python

import pytest
import numpy as np
from minevis.model.elements.dfelement import DFElement


class TestDFElement:
    def test_empty_element(self):
        with pytest.raises(Exception):
            DFElement()

    def test_one_points(self):
        element = DFElement(x=[0], y=[1], z=[2])
        assert len(element.vertices) == 1

        expected = [[0.0, 1.0, 2.0]]

        for i in range(len(expected)):
            assert type(element.vertices[i]) == np.ndarray
            for j in range(3):
                assert element.vertices[i][j] == expected[i][j]

    def test_three_points(self):
        element = DFElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0])
        assert len(element.vertices) == 3

        expected = [[-1.0, 0.0, 0.0],
                    [1.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0]]

        for i in range(len(expected)):
            assert type(element.vertices[i]) == np.ndarray
            for j in range(len(expected[0])):
                assert element.vertices[i][j] == expected[i][j]

    def test_named_element(self):
        name = "NAME"
        extension = "EXT"
        element = DFElement(x=[0], y=[1], z=[2], name=name, ext=extension)
        assert element.name == name
        assert element.extension == extension

    def test_vertices_element(self):
        element = DFElement(vertices=[[0, 1, 2], [3, 4, 5]])

        expected = [[0.0, 1.0, 2.0],
                    [3.0, 4.0, 5.0]]

        for i in range(len(expected)):
            for j in range(len(expected[0])):
                assert element.vertices[i][j] == expected[i][j]

    def test_empty_data(self):
        with pytest.raises(Exception):
            DFElement(vertices=[])

        with pytest.raises(Exception):
            DFElement(data={})

    def test_color_dict(self):
        hsv_rb = DFElement.color_from_dict('red-blue')(np.array([0.0, 1.0]))
        hsv_rg = DFElement.color_from_dict('red-green')(np.array([0.0, 1.0]))
        hsv_br = DFElement.color_from_dict('blue-red')(np.array([0.0, 1.0]))
        hsv_gr = DFElement.color_from_dict('green-red')(np.array([0.0, 1.0]))

        assert hsv_rb[0] == 0.0 / 3.0
        assert hsv_rb[1] == 2.0 / 3.0

        assert hsv_rg[0] == 0.0 / 3.0
        assert hsv_rg[1] == 1.0 / 3.0

        assert hsv_br[0] == 2.0 / 3.0
        assert hsv_br[1] == 0.0 / 3.0

        assert hsv_gr[0] == 1.0 / 3.0
        assert hsv_gr[1] == 0.0 / 3.0

    def test_colormap(self):
        element = DFElement(vertices=[[0, 1, 2], [3, 4, 5], [6, 7, 8]], values=[0, 1, 2])
        assert element.colormap == 'red-blue'
        assert element.color[0][0] == 1.0
        assert element.color[0][1] == 0.0
        assert element.color[0][2] == 0.0

        assert element.color[2][0] == 0.0
        assert element.color[2][1] == 0.0
        assert element.color[2][2] == 1.0

        element.colormap = 'green-red'
        assert element.colormap == 'green-red'
        assert element.color[0][0] == 0.0
        assert element.color[0][1] == 1.0
        assert element.color[0][2] == 0.0

        assert element.color[2][0] == 1.0
        assert element.color[2][1] == 0.0
        assert element.color[2][2] == 0.0

    def test_vmin_vmax(self):
        element = DFElement(vertices=[[0, 1, 2], [3, 4, 5], [6, 7, 8]], values=[0, 1, 2], vmin=0, vmax=1)
        assert element.vmin == 0
        assert element.vmax == 1

        assert element.colormap == 'red-blue'
        assert element.color[0][0] == 1.0
        assert element.color[0][1] == 0.0
        assert element.color[0][2] == 0.0

        assert element.color[1][0] == 0.0
        assert element.color[1][1] == 0.0
        assert element.color[1][2] == 1.0

        assert element.color[2][0] == 0.0
        assert element.color[2][1] == 0.0
        assert element.color[2][2] == 1.0

    def test_setters(self):
        element = DFElement(vertices=[[0, 1, 2]])
        element.name = 'name123'
        element.extension = 'off'
        element.alpha = 0.8

        assert element.name == 'name123'
        assert element.extension == 'off'
        assert element.alpha == 0.8

    def test_color_rgba(self):
        element = DFElement(vertices=[[0, 1, 2]])

        assert element.color[0] == element.rgba[0]
        assert element.color[1] == element.rgba[1]
        assert element.color[2] == element.rgba[2]
        assert element.alpha == element.rgba[3]

        element.rgba = [1.0, 0.9, 0.8, 0.7]

        assert element.color[0] == element.rgba[0] == 1.0
        assert element.color[1] == element.rgba[1] == 0.9
        assert element.color[2] == element.rgba[2] == 0.8
        assert element.alpha == element.rgba[3] == 0.7

    def test_autocolor(self):
        data = {'x': [0.0, 2.0, 4.0, 6.0, 8.0, 10.0],
                'y': [0.0, 0.0, 0.0, 3.0, 3.0, 1.0],
                'z': [0.0, 3.0, 3.0, 3.0, 3.0, 3.0],
                'val': [0.0, 2.0, 4.0, 6.0, 8.0, 10.0]}

        element = DFElement(data=data, vmin=4.0, vmax=8.0, colormap='red-blue')

        expected = [
                    [1.0, 0.0, 0.0],  # Red if val < min
                    [1.0, 0.0, 0.0],
                    [1.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0],  # Green if vmin < val < vmax
                    [0.0, 0.0, 1.0],  # Blue if val > max
                    [0.0, 0.0, 1.0],
                    ]

        for i in range(len(expected)):
            for j in range(len(expected[0])):
                assert element.color[i][j] == expected[i][j]

    def test_enabled_properties(self):
        element = DFElement(vertices=[[0, 1, 2]])
        for prop in ['alpha', 'color']:
            assert prop in element.enabled_properties

    def test_hacky_utilities(self):
        element = DFElement(vertices=[[0, 1, 2]])
        assert element.alpha == 1.0
        assert element.get_property('alpha') == 1.0

        element.set_property('alpha', 0.8)
        assert element.alpha == 0.8
        assert element.get_property('alpha') == 0.8

        with pytest.raises(Exception):
            element.set_property('wrong', 0.0)

        with pytest.raises(Exception):
            element.get_property('wrong')
