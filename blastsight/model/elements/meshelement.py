#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import meshcut
import numpy as np

from .. import utils
from .element import Element


class MeshElement(Element):
    def __init__(self, *args, **kwargs):
        """
        MeshElement is a class inheriting from Element.

        {
            'data': {
                'x': list[float],
                'y': list[float],
                'z': list[float],
                'indices': list[int]
            }
            'properties': {
                'color': list[float],
                'alpha': float
            },
            'metadata': {
                'id': int,
                'name': str or None,
                'extension': str or None
            }
        }
        """
        super().__init__(*args, **kwargs)

    """
    Element filling
    """
    def _fill_element(self, *args, **kwargs) -> None:
        # Vertices
        msg = f'Data must contain ["x", "y", "z"] or "vertices", got {list(kwargs.keys())}.'

        if 'vertices' in kwargs.keys():
            self._fill_as_vertices(*args, **kwargs)
            self._fill_indices(*args, **kwargs)
        elif 'x' in kwargs.keys() and 'y' in kwargs.keys() and 'z' in kwargs.keys():
            self._fill_as_xyz(*args, **kwargs)
            self._fill_indices(*args, **kwargs)
        elif 'data' in kwargs.keys():
            self._fill_as_data(*args, **kwargs)
        else:
            raise KeyError(msg)

    def _fill_indices(self, *args, **kwargs) -> None:
        # Indices
        msg = f'Data must contain "indices", got {list(kwargs.keys())}.'

        if 'indices' in kwargs.keys() and 'data' not in kwargs.keys():
            self.indices = kwargs.get('indices', [])
        else:
            raise KeyError(msg)

    def _fill_as_data(self, *args, **kwargs) -> None:
        data = kwargs.get('data', {})
        self.vertices = data.get('vertices', [])
        self.indices = data.get('indices', [])

    def _check_integrity(self) -> None:
        super()._check_integrity()
        if self.x.size != self.indices.max() + 1:
            raise ValueError('Wrong number of indices for mesh.')

    """
    Data
    """
    @property
    def indices(self) -> np.array:
        return self.data.get('indices', np.empty(0))

    @indices.setter
    def indices(self, indices) -> None:
        # GL_UNSIGNED_INT = np.uint32
        self.data['indices'] = np.array(indices, np.uint32)

    """
    Utilities
    """
    @property
    def volume(self) -> float:
        # Idea from https://www.geometrictools.com/Documentation/PolyhedralMassProperties.pdf
        # Optimizations taken from https://github.com/mikedh/trimesh/blob/master/trimesh/triangles.py
        triangles = self.vertices[self.indices]

        vectors = np.diff(triangles, axis=1)
        crosses = np.cross(vectors[:, 0], vectors[:, 1])
        del vectors

        # This is equivalent but faster than triangles.sum(axis=1)
        f1 = triangles[:, 0, :] + triangles[:, 1, :] + triangles[:, 2, :]
        del triangles

        # Seems very similar to determinant calculation
        volume = (crosses[:, 0] * f1[:, 0]).sum() / 6.0
        del crosses
        del f1

        return abs(volume)

    def slice_with_plane(self, origin: np.ndarray, normal: np.ndarray) -> list:
        # Returns a list with the slices (in case we have a concave mesh)

        def intersect_edges(vertices_a: np.ndarray, vertices_b: np.ndarray) -> np.ndarray:
            # Returns a mask of all edges that *might* be sliced by the plane
            # Adapted from https://en.wikipedia.org/wiki/Line%E2%80%93plane_intersection
            epsilon = 1e-6

            diff_dot_n = np.dot(origin - vertices_a, normal)
            l_dot_n = np.dot(vertices_b - vertices_a, normal)
            t = diff_dot_n / l_dot_n

            # Edge is completely contained in plane
            mask_full = abs(l_dot_n) < epsilon
            mask_full &= abs(diff_dot_n) < epsilon

            # One intersection
            mask_point = 0.0 <= t
            mask_point &= t <= 1.0

            return mask_full | mask_point

        def preprocess_triangles(triangles: np.ndarray) -> np.ndarray:
            # Pre-processes the triangles by each of their edges
            mask_a = intersect_edges(triangles[:, 0], triangles[:, 1])
            mask_b = intersect_edges(triangles[:, 1], triangles[:, 2])
            mask_c = intersect_edges(triangles[:, 2], triangles[:, 0])

            return mask_a | mask_b | mask_c

        mask = preprocess_triangles(self.vertices[self.indices])

        try:
            return meshcut.cross_section(self.vertices, self.indices[mask], np.array(origin), np.array(normal))
        except AssertionError:
            # Meshcut doesn't want to slice
            print(f'WARNING: Mesh {self.name} (id = {self.id}) cannot be sliced, fix your mesh!')
            return []

    def intersect_with_ray(self, origin: np.ndarray, ray: np.ndarray) -> np.ndarray:
        # Early AABB detection test
        if not utils.aabb_intersection(origin, ray, *self.bounding_box):
            return np.empty(0)

        return self.vectorized_intersection(origin, ray)

    def vectorized_intersection(self, origin: np.ndarray, ray: np.ndarray) -> np.ndarray:
        # Idea taken from https://cadxfem.org/inf/Fast%20MinimumStorage%20RayTriangle%20Intersection.pdf
        # Code adapted from https://en.wikipedia.org/wiki/M%C3%B6ller%E2%80%93Trumbore_intersection_algorithm
        # Manually vectorized to benefit from numpy's performance.

        triangles = self.vertices[self.indices]

        # Get individual vertices of each triangle
        vertex0 = triangles[:, 0, :]
        vertex1 = triangles[:, 1, :]
        vertex2 = triangles[:, 2, :]

        edge1 = vertex1 - vertex0
        edge2 = vertex2 - vertex0

        # Note: Both np.inner(a, b).diagonal() and np.dot(a, b.T)
        # run out of memory, but (a * b).sum(axis=1) does not,
        # so we're using that one instead.
        h = np.cross(ray, edge2)
        a = (edge1 * h).sum(axis=1)

        mask = abs(a) > 1e-12  # False => Ray is parallel to triangle.

        # Result of division by zero used deliberately
        with np.errstate(divide='ignore', invalid='ignore'):
            f = 1.0 / a  # Can this be solved in a more elegant way?
            s = origin - vertex0
            u = f * (s * h).sum(axis=1)

            mask = (0.0 <= u) & (u <= 1.0) & mask

            q = np.cross(s, edge1)
            v = f * (ray * q).sum(axis=1)

            mask = (v >= 0.0) & (u + v <= 1.0) & mask

            # At this stage we can compute t to find out where the intersection point is on the line.
            t = f * (edge2 * q).sum(axis=1)

            mask = (t > 1e-12) & mask  # Ray intersections
        return origin + ray * t[mask].reshape(-1, 1)  # Here are the intersections.
