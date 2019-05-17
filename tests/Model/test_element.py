#!/usr/bin/env python

import pytest
import numpy as np
from Model.Elements.element import Element


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

    def test_average_coords(self):
        element = Element(x=[-1, 1, 0], y=[0, 0, 3], z=[0, 0, 0])
        average = element.average_by_coord(element.x, element.y, element.z)

        expected = [0.0, 1.0, 0.0]

        for i in range(len(expected)):
            assert average[i] == expected[i]

    def test_flatten(self):
        element = Element(x=[-1, 1, 0], y=[0, 0, 3], z=[0, 0, 0])
        flattened = Element.flatten(list(element.vertices.tolist()))

        expected = [-1, 0, 0, 1, 0, 0, 0, 3, 0]

        for i in range(len(expected)):
            assert flattened[i] == expected[i]

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
