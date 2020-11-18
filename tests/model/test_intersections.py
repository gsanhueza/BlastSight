#!/usr/bin/env python

import numpy as np

from blastsight.model.intersections import Intersections
from blastsight.model.elements.meshelement import MeshElement


class TestIntersections:
    # Origins
    origin = np.array([0.0, 0.5, 10.0])
    origin_low = np.array([0.0, -0.1, 10.0])
    origin_translated = np.array([10.0, 0.5, 1.0])

    # Rays
    ray = np.array([0.0, 0.0, -1.0])
    ray_reversed = np.array([0.0, 0.0, 1.0])
    ray_oblique = np.array([0.6, 0.0, -0.8])
    ray_low = np.array([0.0, 0.8, -0.9])
    ray_perpendicular = np.array([1.0, 0.0, 0.0])

    # Triangle
    vertices = np.array([[-1.0, 0.0, 0.0],
                         [1.0, 0.0, 0.0],
                         [0.0, 1.0, 0.0],
                         [0.0, -1.0, 0.0]])

    triangle = vertices.view(np.ndarray)[[0, 1, 2]]
    triangle_low = vertices.view(np.ndarray)[[0, 3, 1]]
    triangle_degenerate = vertices.view(np.ndarray)[[0, 0, 0]]

    square = MeshElement(vertices=vertices, indices=[[0, 1, 2], [0, 3, 1]])

    # Tetrahedron
    vertices = np.array([[-1.0, 0.0, 0.0],
                         [1.0, 0.0, 0.0],
                         [0.0, 1.0, 0.0],
                         [0.0, 0.5, 0.5]])
    indices = [[0, 1, 2], [0, 1, 3], [1, 2, 3], [2, 0, 3]]

    tetrahedron = MeshElement(vertices=vertices, indices=indices)

    def test_plane_intersection(self):
        for expected, actual in zip([0.0, 0.5, 0.0],
                                    Intersections.ray_with_plane(self.origin, self.ray,
                                                                 plane_normal=np.array([0.0, 0.0, 1.0]), plane_d=0.0)):
            assert expected == actual

        for expected, actual in zip([10.0, 0.5, 0.0],
                                    Intersections.ray_with_plane(self.origin_translated, self.ray,
                                                                 plane_normal=np.array([0.0, 0.0, 1.0]), plane_d=0.0)):
            assert expected == actual

    def test_aabb_intersection(self):
        assert Intersections.aabb_intersection(self.origin, self.ray, *self.square.bounding_box)
        assert Intersections.aabb_intersection(self.origin, self.ray, *self.tetrahedron.bounding_box)

        assert not Intersections.aabb_intersection(self.origin, self.ray_low, *self.tetrahedron.bounding_box)
        assert not Intersections.aabb_intersection(self.origin, self.ray_perpendicular, *self.tetrahedron.bounding_box)
        assert not Intersections.aabb_intersection(self.origin_translated, self.ray, *self.tetrahedron.bounding_box)
        assert not Intersections.aabb_intersection(self.origin_translated, self.ray_oblique, *self.tetrahedron.bounding_box)
        assert not Intersections.aabb_intersection(self.origin, self.ray_oblique, *self.tetrahedron.bounding_box)

    def test_triangles_intersection(self):
        assert 1 == len(Intersections.ray_with_triangles(self.origin, self.ray, self.square.triangles))
        assert 2 == len(Intersections.ray_with_triangles(self.origin, self.ray, self.tetrahedron.triangles))

        assert 0 == len(Intersections.ray_with_triangles(self.origin, self.ray_low, self.tetrahedron.triangles))
        assert 0 == len(Intersections.ray_with_triangles(self.origin, self.ray_perpendicular, self.tetrahedron.triangles))
        assert 0 == len(Intersections.ray_with_triangles(self.origin_translated, self.ray, self.tetrahedron.triangles))
        assert 0 == len(Intersections.ray_with_triangles(self.origin_translated, self.ray_oblique, self.tetrahedron.triangles))
        assert 0 == len(Intersections.ray_with_triangles(self.origin, self.ray_oblique, self.tetrahedron.triangles))
