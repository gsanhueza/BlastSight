#!/usr/bin/env python

from caseron.model.utils import *
from caseron.model.elements.meshelement import MeshElement


class TestUtils:
    # Triangle
    vertices = np.array([[-1.0, 0.0, 0.0],
                         [1.0, 0.0, 0.0],
                         [0.0, 1.0, 0.0],
                         [0.0, -1.0, 0.0]])

    triangle = vertices.view(np.ndarray)[[0, 1, 2]]
    triangle_low = vertices.view(np.ndarray)[[0, 3, 1]]
    triangle_degenerate = vertices.view(np.ndarray)[[0, 0, 0]]

    mesh_element = MeshElement(vertices=vertices, indices=[[0, 1, 2], [0, 3, 1]])

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

    def test_mesh_intersection(self):
        assert mesh_intersection(self.origin, self.ray, self.mesh_element).size > 0
        assert mesh_intersection(self.origin, self.ray_reversed, self.mesh_element).size == 0
        assert mesh_intersection(self.origin, self.ray_low, self.mesh_element).size == 0
        assert mesh_intersection(self.origin, self.ray_perpendicular, self.mesh_element).size == 0
        assert mesh_intersection(self.origin_translated, self.ray, self.mesh_element).size == 0
        assert mesh_intersection(self.origin_translated, self.ray_oblique, self.mesh_element).size == 0
        assert mesh_intersection(self.origin, self.ray_oblique, self.mesh_element).size == 0
        assert mesh_intersection(self.origin_translated, self.ray, self.tetrahedron).size == 0

    def test_triangle_intersection(self):
        assert triangle_intersection(self.origin, self.ray, self.triangle) is not None
        assert triangle_intersection(self.origin, self.ray_reversed, self.triangle) is None
        assert triangle_intersection(self.origin, self.ray_low, self.triangle_low) is None
        assert triangle_intersection(self.origin, self.ray_low, self.triangle) is None
        assert triangle_intersection(self.origin_translated, self.ray, self.triangle) is None
        assert triangle_intersection(self.origin, self.ray_oblique, self.triangle) is None
        assert triangle_intersection(self.origin, self.ray, self.triangle_degenerate) is None
        assert triangle_intersection(self.origin_low, self.ray, self.triangle) is None

    def test_aabb_intersection(self):
        assert aabb_intersection(self.origin, self.ray, *self.tetrahedron.bounding_box)
        assert not aabb_intersection(self.origin, self.ray_low, *self.tetrahedron.bounding_box)
        assert not aabb_intersection(self.origin, self.ray_perpendicular, *self.tetrahedron.bounding_box)
        assert not aabb_intersection(self.origin_translated, self.ray, *self.tetrahedron.bounding_box)
        assert not aabb_intersection(self.origin_translated, self.ray_oblique, *self.tetrahedron.bounding_box)
        assert not aabb_intersection(self.origin, self.ray_oblique, *self.tetrahedron.bounding_box)
