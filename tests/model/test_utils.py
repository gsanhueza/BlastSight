#!/usr/bin/env python

import numpy as np
from blastsight.model import utils
from blastsight.model.elements.meshelement import MeshElement


class TestUtils:
    # Triangle
    vertices = np.array([[-1.0, 0.0, 0.0],
                         [1.0, 0.0, 0.0],
                         [0.0, 1.0, 0.0],
                         [0.0, -1.0, 0.0]])

    triangle = vertices.view(np.ndarray)[[0, 1, 2]]
    triangle_low = vertices.view(np.ndarray)[[0, 3, 1]]
    triangle_degenerate = vertices.view(np.ndarray)[[0, 0, 0]]

    mesh = MeshElement(vertices=vertices, indices=[[0, 1, 2], [0, 3, 1]])

    # Tetrahedron
    vertices = np.array([[-1.0, 0.0, 0.0],
                         [1.0, 0.0, 0.0],
                         [0.0, 1.0, 0.0],
                         [0.0, 0.5, 0.5]])
    indices = [[0, 1, 2], [0, 1, 3], [1, 2, 3], [2, 0, 3]]

    tetrahedron = MeshElement(vertices=vertices, indices=indices)

    origin = np.array([0.0, 0.5, 10.0])
    origin_low = np.array([0.0, -0.1, 10.0])
    origin_translated = np.array([10.0, 0.5, 1.0])

    ray = np.array([0.0, 0.0, -1.0])
    ray_reversed = np.array([0.0, 0.0, 1.0])
    ray_oblique = np.array([0.6, 0.0, -0.8])
    ray_low = np.array([0.0, 0.8, -0.9])
    ray_perpendicular = np.array([1.0, 0.0, 0.0])

    def test_aabb_intersection(self):
        assert utils.aabb_intersection(self.origin, self.ray, *self.tetrahedron.bounding_box)
        assert not utils.aabb_intersection(self.origin, self.ray_low, *self.tetrahedron.bounding_box)
        assert not utils.aabb_intersection(self.origin, self.ray_perpendicular, *self.tetrahedron.bounding_box)
        assert not utils.aabb_intersection(self.origin_translated, self.ray, *self.tetrahedron.bounding_box)
        assert not utils.aabb_intersection(self.origin_translated, self.ray_oblique, *self.tetrahedron.bounding_box)
        assert not utils.aabb_intersection(self.origin, self.ray_oblique, *self.tetrahedron.bounding_box)

    def test_closest_points(self):
        assert utils.closest_point_to(self.origin, np.array([])) is None

        point_array = np.array([self.origin, self.origin_low, self.origin_translated])
        for i in range(3):
            assert utils.closest_point_to(self.origin, point_array)[i] == self.origin[i]
            assert utils.closest_point_to(self.origin_low, point_array)[i] == self.origin_low[i]
            assert utils.closest_point_to(self.origin_translated, point_array)[i] == self.origin_translated[i]

    def test_distances_between_points(self):
        assert utils.distances_between(self.origin, np.array([])) is None

        point_array = np.array([self.origin, self.origin_low, self.origin_translated])
        distances = utils.distances_between(self.origin, point_array)

        assert len(distances) == len(point_array)
        assert distances[0] < distances[1]
        assert distances[0] < distances[2]
        assert distances[1] < distances[2]
