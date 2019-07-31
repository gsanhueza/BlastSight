#!/usr/bin/env python

import numpy as np
from random import random

from .element import Element


class MeshElement(Element):
    def __init__(self, *args, **kwargs):
        self._indices: np.ndarray = np.array([], np.float32)

        super().__init__(*args, **kwargs)

        self.indices = kwargs.get('indices', [])
        self.values = kwargs.get('color', list(map(lambda x: random(), range(3))))

        assert self.x.size == self.indices.max() + 1

    @property
    def indices(self) -> np.array:
        return self._indices

    @indices.setter
    def indices(self, indices):
        self._indices = np.array(indices, np.uint32)  # GL_UNSIGNED_INT = np.uint32

    def volume(self, **kwargs):
        method = kwargs.get('method', 'fast')

        if method == 'fast':
            return self.volume_integral()
        elif method == 'low_memory':
            return self.volume_determinant()
        else:
            raise Exception('Method not defined!')

    def volume_determinant(self):
        # Idea from https://stackoverflow.com/questions/1838401/general-formula-to-calculate-polyhedron-volume
        # Taken from http://melax.github.io/volint.html

        # This works with constant memory, but it's horribly slow
        volume = 0
        triangles = self.vertices.view(np.ndarray)[self.indices]

        for triangle in triangles:
            volume += np.linalg.det(np.matrix(triangle))
        return abs(volume / 6.0)

    def volume_integral(self):
        # Idea from https://www.geometrictools.com/Documentation/PolyhedralMassProperties.pdf
        # Taken from https://github.com/mikedh/trimesh/blob/master/trimesh/triangles.py
        # (Give credit where it's due)

        # This is fast! But uses more memory
        triangles = self.vertices.view(np.ndarray)[self.indices]

        vectors = np.diff(triangles, axis=1)
        crosses = np.cross(vectors[:, 0], vectors[:, 1])

        # These are the subexpressions of the integral
        # This is equivalent but 7x faster than triangles.sum(axis=1)
        f1 = triangles[:, 0, :] + triangles[:, 1, :] + triangles[:, 2, :]

        # For the the first vertex of every triangle:
        # Triangles[:,0,:] will give rows like [[x0, y0, z0], ...]

        # For the x coordinates of every triangle
        # Triangles[:,:,0] will give rows like [[x0, x1, x2], ...]
        f2 = (triangles[:, 0, :] ** 2 +
              triangles[:, 1, :] ** 2 +
              triangles[:, 0, :] * triangles[:, 1, :] +
              triangles[:, 2, :] * f1)
        f3 = ((triangles[:, 0, :] ** 3) +
              (triangles[:, 0, :] ** 2) * (triangles[:, 1, :]) +
              (triangles[:, 0, :]) * (triangles[:, 1, :] ** 2) +
              (triangles[:, 1, :] ** 3) +
              (triangles[:, 2, :] * f2))
        g0 = (f2 + (triangles[:, 0, :] + f1) * triangles[:, 0, :])
        g1 = (f2 + (triangles[:, 1, :] + f1) * triangles[:, 1, :])
        g2 = (f2 + (triangles[:, 2, :] + f1) * triangles[:, 2, :])
        integral = np.zeros((10, len(f1)))
        integral[0] = crosses[:, 0] * f1[:, 0]
        integral[1:4] = (crosses * f2).T
        integral[4:7] = (crosses * f3).T

        for i in range(3):
            triangle_i = np.mod(i + 1, 3)
            integral[i + 7] = crosses[:, i] * (
                    (triangles[:, 0, triangle_i] * g0[:, i]) +
                    (triangles[:, 1, triangle_i] * g1[:, i]) +
                    (triangles[:, 2, triangle_i] * g2[:, i]))

        coefficients = 1.0 / np.array([6, 24, 24, 24, 60, 60, 60, 120, 120, 120], np.float64)
        integrated = integral.sum(axis=1) * coefficients

        volume = integrated[0]

        return abs(volume)
