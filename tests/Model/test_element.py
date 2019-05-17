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
        list_vertices = element.vertices
        assert len(list_vertices) == 1

        v = list_vertices[0]
        assert type(v) == np.ndarray
        assert v[0] == 0
        assert v[1] == 1
        assert v[2] == 2

    def test_one_triangle(self):
        element = Element(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0])
        list_vertices = element.vertices
        assert len(list_vertices) == 3

        for v in list_vertices:
            assert type(v) == np.ndarray

        assert all(list_vertices[0].tolist()) == all([-1.0, 0.0, 0.0])
        assert all(list_vertices[1].tolist()) == all([1.0, 0.0, 0.0])
        assert all(list_vertices[2].tolist()) == all([0.0, 1.0, 0.0])

    def test_average_coords(self):
        element = Element(x=[-1, 1, 0], y=[0, 0, 3], z=[0, 0, 0])
        average = element.average_by_coord(element.x, element.y, element.z)
        assert average[0] == 0
        assert average[1] == 1
        assert average[2] == 0

    def test_flatten(self):
        element = Element(x=[-1, 1, 0], y=[0, 0, 3], z=[0, 0, 0])
        vertices = element.vertices

        flattened_vertices = Element.flatten(list(vertices.tolist()))

        assert flattened_vertices[0] == -1
        assert flattened_vertices[1] == 0
        assert flattened_vertices[2] == 0

        assert flattened_vertices[3] == 1
        assert flattened_vertices[4] == 0
        assert flattened_vertices[5] == 0

        assert flattened_vertices[6] == 0
        assert flattened_vertices[7] == 3
        assert flattened_vertices[8] == 0

    def test_named_element(self):
        name = "NAME"
        extension = "EXT"
        element = Element(x=[0], y=[1], z=[2], name=name, ext=extension)
        assert element.name == name
        assert element.ext == extension

    def test_vertices_element(self):
        element = Element(vertices=[[0, 1, 2], [3, 4, 5]])
        assert element.vertices[0][0] == 0.0
        assert element.vertices[0][1] == 1.0
        assert element.vertices[0][2] == 2.0

        assert element.vertices[1][0] == 3.0
        assert element.vertices[1][1] == 4.0
        assert element.vertices[1][2] == 5.0

    def test_empty_vertices(self):
        with pytest.raises(Exception):
            Element(vertices=[])

    def test_set_vertices(self):
        element = Element(vertices=[[0, 1, 2]])
        element.vertices = [[9, 8, 7], [6, 5, 4]]

        assert element.vertices[0][0] == 9.0
        assert element.vertices[0][1] == 8.0
        assert element.vertices[0][2] == 7.0

        assert element.vertices[1][0] == 6.0
        assert element.vertices[1][1] == 5.0
        assert element.vertices[1][2] == 4.0
