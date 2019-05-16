#!/usr/bin/env python

import numpy as np
import pytest
from Model.Mesh.meshelement import MeshElement


class TestMeshElement:
    def test_empty_mesh(self):
        with pytest.raises(Exception):
            MeshElement()

    def test_single_triangle(self):
        element = MeshElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])

        list_vertices = element.get_vertices()
        assert len(list_vertices) == 3

        for v in list_vertices:
            assert type(v) == np.ndarray

        assert all(list_vertices[0].tolist()) == all([-1.0, 0.0, 0.0])
        assert all(list_vertices[1].tolist()) == all([1.0, 0.0, 0.0])
        assert all(list_vertices[2].tolist()) == all([0.0, 1.0, 0.0])

        list_indices = element.get_indices()
        assert len(list_indices) == 1
        index = list_indices[0]
        assert index[0] == 0
        assert index[1] == 1
        assert index[2] == 2

    def test_shared_triangles(self):
        element = MeshElement(x=[-1, 1, 0, 2], y=[0, 0, 1, 1], z=[0, 0, 0, 0], indices=[[0, 1, 2], [1, 3, 2]])

        list_vertices = element.get_vertices()
        assert len(list_vertices) == 4

        for v in list_vertices:
            assert type(v) == np.ndarray

        assert all(list_vertices[0].tolist()) == all([-1.0, 0.0, 0.0])
        assert all(list_vertices[1].tolist()) == all([1.0, 0.0, 0.0])
        assert all(list_vertices[2].tolist()) == all([0.0, 1.0, 0.0])
        assert all(list_vertices[2].tolist()) == all([2.0, 1.0, 0.0])

        list_indices = element.get_indices()
        assert len(list_indices) == 2

        index_a = list_indices[0]
        assert index_a[0] == 0
        assert index_a[1] == 1
        assert index_a[2] == 2

        index_b = list_indices[1]
        assert index_b[0] == 1
        assert index_b[1] == 3
        assert index_b[2] == 2

    def test_wrong_mesh(self):
        with pytest.raises(Exception):
            MeshElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0], indices=[[0, 1, 2]])

        with pytest.raises(Exception):
            MeshElement(x=[-1, 1, 0], y=[0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])

        with pytest.raises(Exception):
            MeshElement(x=[-1, 1], y=[0, 0], z=[0, 0], indices=[[0, 1, 2]])

    def test_centroid_single(self):
        element = MeshElement(x=[-1, 1, 0], y=[0, 0, 3], z=[0, 0, 0], indices=[[0, 1, 2]])
        centroid = element.get_centroid()

        assert centroid[0] == 0
        assert centroid[1] == 1
        assert centroid[2] == 0
