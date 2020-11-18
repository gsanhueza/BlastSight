#!/usr/bin/env python

import numpy as np

from blastsight.model.intersections import Intersections
from blastsight.model.elements.meshelement import MeshElement


class TestIntersections:
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
        assert Intersections.aabb_intersection(self.origin, self.ray, *self.tetrahedron.bounding_box)
        assert not Intersections.aabb_intersection(self.origin, self.ray_low, *self.tetrahedron.bounding_box)
        assert not Intersections.aabb_intersection(self.origin, self.ray_perpendicular, *self.tetrahedron.bounding_box)
        assert not Intersections.aabb_intersection(self.origin_translated, self.ray, *self.tetrahedron.bounding_box)
        assert not Intersections.aabb_intersection(self.origin_translated, self.ray_oblique, *self.tetrahedron.bounding_box)
        assert not Intersections.aabb_intersection(self.origin, self.ray_oblique, *self.tetrahedron.bounding_box)
