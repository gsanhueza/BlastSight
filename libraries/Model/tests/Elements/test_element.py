#!/usr/bin/env python

import pytest
import numpy as np
from libraries.Model.Elements.element import Element


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
        assert element.ext == extension

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
        element.ext = 'off'
        element.alpha = 0.8

        assert element.name == 'name123'
        assert element.ext == 'off'
        assert element.alpha == 0.8
