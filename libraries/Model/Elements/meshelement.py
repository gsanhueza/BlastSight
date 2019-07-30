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

    # Taken from https://stackoverflow.com/questions/1838401/general-formula-to-calculate-polyhedron-volume
    def volume(self):
        sum_det = 0.0
        origin = self.centroid

        for idx in self.indices:
            # Generate matrix for determinant calculation
            triangle = [t + [1.0] for t in self.vertices[idx].tolist()]
            triangle.append(origin.tolist() + [1.0])

            # FIXME CCW or CW consistency is key
            sum_det += np.linalg.det(np.matrix(triangle))

        return abs(sum_det / 6.0)
