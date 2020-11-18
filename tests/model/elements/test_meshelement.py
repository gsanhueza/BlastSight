#!/usr/bin/env python

import numpy as np
import pytest
from blastsight.model.elements.meshelement import MeshElement


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
            for j in range(len(expected[0])):
                assert element.vertices[i][j] == expected[i][j]

        assert len(element.indices) == 1

        expected = [[0, 1, 2]]

        for i in range(len(expected)):
            for j in range(len(expected[0])):
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
            for j in range(len(expected[0])):
                assert element.vertices[i][j] == expected[i][j]

        assert len(element.indices) == 2

        expected = [[0, 1, 2], [1, 3, 2]]

        for i in range(len(expected)):
            for j in range(len(expected[0])):
                assert element.indices[i][j] == expected[i][j]

    def test_load_as_xyz(self):
        element = MeshElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])

        assert len(element.vertices) == 3
        assert len(element.indices) == 1

    def test_load_as_vertices(self):
        element = MeshElement(vertices=[[-1, 1, 0], [0, 0, 1], [0, 0, 0]], indices=[[0, 1, 2]])

        assert len(element.vertices) == 3
        assert len(element.indices) == 1

    def test_load_as_triangles(self):
        element = MeshElement(triangles=[[-1, 1, 0], [0, 0, 1], [0, 0, 0]])

        assert len(element.vertices) == 3
        assert len(element.indices) == 1

    def test_load_as_data(self):
        data = {
            'vertices': [[-1, 1, 0], [0, 0, 1], [0, 0, 0]],
            'indices': [[0, 1, 2]],
        }
        element = MeshElement(data=data)

        assert len(element.vertices) == 3
        assert len(element.indices) == 1

    def test_wrong_mesh(self):
        with pytest.raises(ValueError):
            MeshElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0], indices=[[0, 1, 2]])

        with pytest.raises(ValueError):
            MeshElement(x=[-1, 1, 0], y=[0, 1], z=[0, 0, 0], indices=[[0, 1, 2]])

        with pytest.raises(ValueError):
            MeshElement(x=[-1, 1], y=[0, 0], z=[0, 0], indices=[[0, 1, 2]])

        with pytest.raises(KeyError):
            MeshElement(x=[-1, 1], y=[0, 0], z=[0, 0])

    def test_center(self):
        element = MeshElement(x=[-1, 1, 0], y=[0, 0, 3], z=[0, 0, 0], indices=[[0, 1, 2]])

        expected = [0.0, 1.5, 0.0]
        for i in range(len(expected)):
            assert element.center[i] == expected[i]

    def test_centroid(self):
        element = MeshElement(x=[-1, 1, 0], y=[0, 0, 3], z=[0, 0, 0], indices=[[0, 1, 2]])

        expected = [0.0, 1.0, 0.0]
        for i in range(len(expected)):
            assert element.centroid[i] == expected[i]

    def test_set_color(self):
        element = MeshElement(x=[-1, 1, 0], y=[0, 0, 3], z=[0, 0, 0], indices=[[0, 1, 2]])
        assert element.color.size == 3

        element.color = [0, 1, 2]
        assert element.color.size == 3

        # Color = RGB
        expected = [0.0, 1.0, 2.0]
        for i in range(len(expected)):
            assert element.color[i] == expected[i]

        # RGBA
        expected = [0.0, 1.0, 2.0, 1.0]
        for i in range(len(expected)):
            assert element.rgba[i] == expected[i]

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
        volume = element.volume

        assert abs(volume - 8.0) < epsilon
