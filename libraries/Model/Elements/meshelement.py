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
        # Optimizations taken from https://github.com/mikedh/trimesh/blob/master/trimesh/triangles.py

        triangles = self.vertices.view(np.ndarray)[self.indices]

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
