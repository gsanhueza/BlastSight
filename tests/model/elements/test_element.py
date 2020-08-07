#!/usr/bin/env python

import pytest
import numpy as np
from blastsight.model.elements.element import Element


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
            for j in range(len(expected[0])):
                assert element.vertices[i][j] == expected[i][j]

    def test_one_triangle(self):
        element = Element(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0])
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
        element = Element(x=[0], y=[1], z=[2], name=name, extension=extension)
        assert element.name == name
        assert element.extension == extension

    def test_vertices_element(self):
        element = Element(vertices=[[0, 1, 2], [3, 4, 5]])

        expected = [[0.0, 1.0, 2.0],
                    [3.0, 4.0, 5.0]]

        for i in range(len(expected)):
            for j in range(len(expected[0])):
                assert element.vertices[i][j] == expected[i][j]

    def test_empty_vertices(self):
        with pytest.raises(Exception):
            Element(vertices=[])

    def test_data_element(self):
        element = Element(data={'x': [0, 3], 'y': [1, 4], 'z': [2, 5]})

        expected = [[0.0, 1.0, 2.0],
                    [3.0, 4.0, 5.0]]

        for i in range(len(expected)):
            for j in range(len(expected[0])):
                assert element.vertices[i][j] == expected[i][j]

        element = Element(data={'vertices': [[0.0, 1.0, 2.0],
                                             [3.0, 4.0, 5.0]]})

        expected = [[0.0, 1.0, 2.0],
                    [3.0, 4.0, 5.0]]

        for i in range(len(expected)):
            for j in range(len(expected[0])):
                assert element.vertices[i][j] == expected[i][j]

    def test_empty_data(self):
        with pytest.raises(Exception):
            Element(vertices={})

    def test_set_vertices(self):
        element = Element(vertices=[[0, 1, 2]])
        element.vertices = [[9, 8, 7], [6, 5, 4]]

        expected = [[9.0, 8.0, 7.0],
                    [6.0, 5.0, 4.0]]

        for i in range(len(expected)):
            for j in range(len(expected[0])):
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

        # We check attributes as properties + metadata
        for prop in element.properties.keys():
            assert prop in element.attributes.keys()

        for prop in element.metadata.keys():
            assert prop in element.attributes.keys()

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

    def test_center_centroid(self):
        element = Element(vertices=[[0, 1, 2], [3, 4, 5], [3, 4, 5]])
        assert element.center[0] == 1.5
        assert element.center[1] == 2.5
        assert element.center[2] == 3.5

        assert element.centroid[0] == 2.0
        assert element.centroid[1] == 3.0
        assert element.centroid[2] == 4.0

    def test_getattr_setattr(self):
        element = Element(vertices=[[0, 1, 2]])
        assert element.alpha == 1.0
        assert getattr(element, 'alpha') == 1.0

        setattr(element, 'alpha', 0.8)
        assert element.alpha == 0.8
        assert getattr(element, 'alpha') == 0.8

        with pytest.raises(Exception):
            setattr(element, 'wrong', 0.0)

        with pytest.raises(Exception):
            getattr(element, 'wrong')
