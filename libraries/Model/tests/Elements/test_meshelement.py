#!/usr/bin/env python

import numpy as np
import pytest
from libraries.Model.Elements.meshelement import MeshElement


class TestMeshElement:
    def test_empty_mesh(self):
        with pytest.raises(Exception):
            MeshElement()

    def test_single_triangle(self):
        element = MeshElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])

        assert len(element.vertices) == 3

        for v in element.vertices:
            assert type(v) == np.ndarray

        expected = [[-1.0, 0.0, 0.0],
                    [1.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0]]

        for i in range(len(expected)):
            for j in range(3):
                assert element.vertices[i][j] == expected[i][j]

        assert len(element.indices) == 1

        expected = [[0, 1, 2]]

        for i in range(len(expected)):
            for j in range(3):
                assert element.indices[i][j] == expected[i][j]

    def test_shared_triangles(self):
        element = MeshElement(x=[-1, 1, 0, 2], y=[0, 0, 1, 1], z=[0, 0, 0, 0], indices=[[0, 1, 2], [1, 3, 2]])

        assert len(element.vertices) == 4

        for v in element.vertices:
            assert type(v) == np.ndarray

        expected = [[-1.0, 0.0, 0.0],
                    [1.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0],
                    [2.0, 1.0, 0.0]]

        for i in range(len(expected)):
            for j in range(3):
                assert element.vertices[i][j] == expected[i][j]

        assert len(element.indices) == 2

        expected = [[0, 1, 2], [1, 3, 2]]

        for i in range(len(expected)):
            for j in range(3):
                assert element.indices[i][j] == expected[i][j]

    def test_wrong_mesh(self):
        with pytest.raises(Exception):
            MeshElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0], indices=[[0, 1, 2]])

        with pytest.raises(Exception):
            MeshElement(x=[-1, 1, 0], y=[0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])

        with pytest.raises(Exception):
            MeshElement(x=[-1, 1], y=[0, 0], z=[0, 0], indices=[[0, 1, 2]])

    def test_centroid_single(self):
        element = MeshElement(x=[-1, 1, 0], y=[0, 0, 3], z=[0, 0, 0], indices=[[0, 1, 2]])

        expected = [0.0, 1.0, 0.0]
        for i in range(len(expected)):
            assert element.centroid[i] == expected[i]

    def test_set_values(self):
        element = MeshElement(x=[-1, 1, 0], y=[0, 0, 3], z=[0, 0, 0], indices=[[0, 1, 2]])
        assert element.values.size == 3
        assert type(element.values[0]) == np.float32

        element.values = [0, 1, 2]
        assert element.values.size == 3
        assert type(element.values[0]) == np.float32

        expected = [0.0, 1.0, 2.0]
        for i in range(len(expected)):
            assert element.values[i] == expected[i]

    def test_volume(self):
        # Cube
        element = MeshElement(vertices=[[-1.0, -1.0, -1.0],
                                        [+1.0, -1.0, -1.0],
                                        [-1.0, +1.0, -1.0],
                                        [+1.0, +1.0, -1.0],
                                        [-1.0, -1.0, +1.0],
                                        [+1.0, -1.0, +1.0],
                                        [-1.0, +1.0, +1.0],
                                        [+1.0, +1.0, +1.0],
                                        ],
                              indices=[[0, 1, 2],
                                       [2, 1, 3],
                                       [4, 6, 5],
                                       [5, 6, 7],

                                       [1, 5, 3],
                                       [3, 5, 7],
                                       [0, 2, 4],
                                       [4, 2, 6],

                                       [2, 3, 6],
                                       [6, 3, 7],
                                       [4, 1, 0],
                                       [4, 5, 1],
                                       ])

        epsilon = 0.00001
        vol_det = element.volume(method='low_memory')
        vol_int = element.volume(method='fast')

        with pytest.raises(Exception):
            element.volume(method='not_a_method')

        assert abs(vol_det - 8.0) < epsilon
        assert abs(vol_int - 8.0) < epsilon
