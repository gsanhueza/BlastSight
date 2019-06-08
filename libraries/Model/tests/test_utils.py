#!/usr/bin/env python

from libraries.Model.utils import *
from ..Elements.meshelement import MeshElement


class TestUtils:
    mesh = np.array([[-1.0, 0.0, 3.0],
                     [1.0, 0.0, 3.0],
                     [0.0, 1.0, 3.0],
                     [0.0, -1.0, 3.0]], np.float32)
    triangle = np.array([mesh[0], mesh[1], mesh[2]], np.float32)
    triangle_low = np.array([mesh[0], mesh[3], mesh[1]], np.float32)

    mesh_element = MeshElement(vertices=mesh, indices=[[0, 1, 2], [0, 3, 1]])

    origin = np.array([0.0, 0.5, 0.0], np.float32)
    origin_translated = np.array([10.0, 0.5, 0.0], np.float32)

    ray = np.array([0.0, 0.0, -1.0], np.float32)
    ray_reversed = np.array([0.0, 0.0, 1.0], np.float32)
    ray_oblique = np.array([0.6, 0.0, -0.8], np.float32)
    ray_low = np.array([0.0, 0.2, -0.9], np.float32)
    ray_perpendicular = np.array([1.0, 0.0, 0.0], np.float32)

    def test_mesh_intersection(self):
        assert mesh_intersection(self.origin, self.ray, self.mesh_element)
        assert mesh_intersection(self.origin, self.ray_reversed, self.mesh_element)
        assert mesh_intersection(self.origin, self.ray_low, self.mesh_element)
        assert not mesh_intersection(self.origin, self.ray_perpendicular, self.mesh_element)
        assert not mesh_intersection(self.origin_translated, self.ray, self.mesh_element)
        assert not mesh_intersection(self.origin, self.ray_oblique, self.mesh_element)

    def test_triangle_intersection(self):
        assert triangle_intersection(self.origin, self.ray, self.triangle)
        assert triangle_intersection(self.origin, self.ray_reversed, self.triangle)
        assert triangle_intersection(self.origin, self.ray_low, self.triangle_low)
        assert not mesh_intersection(self.origin, self.ray_perpendicular, self.mesh_element)
        assert not triangle_intersection(self.origin, self.ray_low, self.triangle)
        assert not triangle_intersection(self.origin_translated, self.ray, self.triangle)
        assert not triangle_intersection(self.origin, self.ray_oblique, self.triangle)

    def test_plane_intersection(self):
        a = np.array(self.triangle[0])
        b = np.array(self.triangle[1])
        c = np.array(self.triangle[2])

        cross = np.cross(b - a, c - b)
        normal = cross / np.linalg.norm(cross)
        d = np.dot(cross, a)

        assert plane_intersection(self.origin, self.ray, normal, d).all() == all(
            np.array([0.0, 0.5, 3.0], np.float32)
        )
