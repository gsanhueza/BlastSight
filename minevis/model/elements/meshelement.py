#!/usr/bin/env python

import numpy as np
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
    def _fill_element(self, *args, **kwargs):
        super()._fill_element(*args, **kwargs)

        if 'indices' not in kwargs.keys():
            raise KeyError('Data must have "indices".')
        self.indices = kwargs.get('indices', [])

    def _check_integrity(self):
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
    def indices(self, indices):
        # GL_UNSIGNED_INT = np.uint32
        self.data['indices'] = np.array(indices, np.uint32)

    """
    Utilities
    """
    def volume(self):
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
