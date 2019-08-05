#!/usr/bin/env python

from libraries.Model.utils import *
from ..Elements.meshelement import MeshElement


class TestUtils:
    mesh = np.array([[-1.0, 0.0, 0.0],
                     [1.0, 0.0, 0.0],
                     [0.0, 1.0, 0.0],
                     [0.0, -1.0, 0.0]], np.float32)

    triangle = mesh.view(np.ndarray)[[0, 1, 2]]
    triangle_low = mesh.view(np.ndarray)[[0, 3, 1]]
    triangle_degenerate = mesh.view(np.ndarray)[[0, 0, 0]]

    mesh_element = MeshElement(vertices=mesh, indices=[[0, 1, 2], [0, 3, 1]])

    origin = np.array([0.0, 0.5, 10.0], np.float32)
    origin_low = np.array([0.0, -0.1, 1.0], np.float32)
    origin_translated = np.array([10.0, 0.5, 10.0], np.float32)

    ray = np.array([0.0, 0.0, -1.0], np.float32)
    ray_reversed = np.array([0.0, 0.0, 1.0], np.float32)
    ray_oblique = np.array([0.6, 0.0, -0.8], np.float32)
    ray_low = np.array([0.0, 0.8, -0.9], np.float32)
    ray_perpendicular = np.array([1.0, 0.0, 0.0], np.float32)

    def test_mesh_intersection(self):
        assert mesh_intersection(self.origin, self.ray, self.mesh_element)
        assert not mesh_intersection(self.origin, self.ray_reversed, self.mesh_element)
        assert not mesh_intersection(self.origin, self.ray_low, self.mesh_element)
        assert not mesh_intersection(self.origin, self.ray_perpendicular, self.mesh_element)
        assert not mesh_intersection(self.origin_translated, self.ray, self.mesh_element)
        assert not mesh_intersection(self.origin, self.ray_oblique, self.mesh_element)

    def test_triangle_intersection(self):
        assert triangle_intersection(self.origin, self.ray, self.triangle)
        assert not triangle_intersection(self.origin, self.ray_reversed, self.triangle)
        assert not triangle_intersection(self.origin, self.ray_low, self.triangle_low)
        assert not triangle_intersection(self.origin, self.ray_low, self.triangle)
        assert not triangle_intersection(self.origin_translated, self.ray, self.triangle)
        assert not triangle_intersection(self.origin, self.ray_oblique, self.triangle)
        assert not triangle_intersection(self.origin, self.ray, self.triangle_degenerate)
        assert not triangle_intersection(self.origin_low, self.ray, self.triangle)
