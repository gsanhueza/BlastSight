#!/usr/bin/env python

import numpy as np
from random import random

from .element import Element


class MeshElement(Element):
    def __init__(self, *args, **kwargs):
        self._indices = None
        self._color = None

        super().__init__(*args, **kwargs)

        self.indices = kwargs.get('indices', [])
        self.color = kwargs.get('color', [random() for _ in range(3)])

        assert self.x.size == self.indices.max() + 1

    @property
    def indices(self) -> np.array:
        return self._indices

    @indices.setter
    def indices(self, indices):
        self._indices = np.array(indices, np.uint32)  # GL_UNSIGNED_INT = np.uint32

    @property
    def color(self) -> np.array:
        return self._color

    @color.setter
    def color(self, val):
        self._color = np.array(val, np.float32)

    @property
    def rgba(self):
        return np.append(self.color, self.alpha)

    def volume(self):
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
