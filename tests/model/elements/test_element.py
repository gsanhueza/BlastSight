#!/usr/bin/env python

import pytest
import numpy as np
from minevis.model.elements.element import Element


class TestElement:
    def test_empty_element(self):
        with pytest.raises(Exception):
            Element()

    def test_one_vertex(self):
        element = Element(x=[0], y=[1], z=[2])
        assert len(element.vertices) == 1

        expected = [[0.0, 1.0, 2.0]]

        for i in range(len(expected)):
            assert type(element.vertices[i]) == np.ndarray
            for j in range(3):
                assert element.vertices[i][j] == expected[i][j]

    def test_one_triangle(self):
        element = Element(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0])
        assert len(element.vertices) == 3

        expected = [[-1.0, 0.0, 0.0],
                    [1.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0]]

        for i in range(len(expected)):
            assert type(element.vertices[i]) == np.ndarray
            for j in range(3):
                assert element.vertices[i][j] == expected[i][j]

    def test_named_element(self):
        name = "NAME"
        extension = "EXT"
        element = Element(x=[0], y=[1], z=[2], name=name, ext=extension)
        assert element.name == name
        assert element.extension == extension

    def test_vertices_element(self):
        element = Element(vertices=[[0, 1, 2], [3, 4, 5]])

        expected = [[0.0, 1.0, 2.0],
                    [3.0, 4.0, 5.0]]

        for i in range(len(expected)):
            for j in range(3):
                assert element.vertices[i][j] == expected[i][j]

    def test_empty_vertices(self):
        with pytest.raises(Exception):
            Element(vertices=[])

    def test_set_vertices(self):
        element = Element(vertices=[[0, 1, 2]])
        element.vertices = [[9, 8, 7], [6, 5, 4]]

        expected = [[9.0, 8.0, 7.0],
                    [6.0, 5.0, 4.0]]

        for i in range(len(expected)):
            for j in range(3):
                assert element.vertices[i][j] == expected[i][j]

    def test_setters(self):
        element = Element(vertices=[[0, 1, 2]])
        element.name = 'name123'
        element.extension = 'off'
        element.alpha = 0.8

        assert element.name == 'name123'
        assert element.extension == 'off'
        assert element.alpha == 0.8

    def test_accessors(self):
        element = Element(vertices=[[0, 1, 2]])
        assert 'x' in element.data.keys()
        assert 'y' in element.data.keys()
        assert 'z' in element.data.keys()

        element.data = {'a': 1, 'b': 2, 'c': 3}
        assert 'a' in element.data.keys()
        assert 'b' in element.data.keys()
        assert 'c' in element.data.keys()
        assert 'x' not in element.data.keys()
        assert 'y' not in element.data.keys()
        assert 'z' not in element.data.keys()

        assert 'color' in element.properties.keys()
        assert 'alpha' in element.properties.keys()

        # We replace data, but we add properties
        element.properties = {'d': 4, 'e': 5}
        assert 'd' in element.properties.keys()
        assert 'e' in element.properties.keys()
        assert 'color' in element.properties.keys()
        assert 'alpha' in element.properties.keys()

    def test_color_rgba(self):
        element = Element(vertices=[[0, 1, 2]])

        assert element.color[0] == element.rgba[0]
        assert element.color[1] == element.rgba[1]
        assert element.color[2] == element.rgba[2]
        assert element.alpha == element.rgba[3]

        element.rgba = [1.0, 0.9, 0.8, 0.7]

        assert element.color[0] == element.rgba[0] == 1.0
        assert element.color[1] == element.rgba[1] == 0.9
        assert element.color[2] == element.rgba[2] == 0.8
        assert element.alpha == element.rgba[3] == 0.7

    def test_enabled_properties(self):
        element = Element(vertices=[[0, 1, 2]])
        for prop in ['alpha', 'color']:
            assert prop in element.enabled_properties

    def test_hacky_utilities(self):
        element = Element(vertices=[[0, 1, 2]])
        assert element.alpha == 1.0
        assert element.get_property('alpha') == 1.0

        element.set_property('alpha', 0.8)
        assert element.alpha == 0.8
        assert element.get_property('alpha') == 0.8

        with pytest.raises(Exception):
            element.set_property('wrong', 0.0)

        with pytest.raises(Exception):
            element.get_property('wrong')
