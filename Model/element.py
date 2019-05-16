#!/usr/bin/env python

import numpy as np
from statistics import mean


class Element:
    def __init__(self, *args, **kwargs):
        if 'vertices' in kwargs.keys():
            self.x, self.y, self.z = zip(*kwargs.get('vertices'))

        elif all(elem in list(kwargs.keys()) for elem in ['x', 'y', 'z']):
            self.x = kwargs.get('x')
            self.y = kwargs.get('y')
            self.z = kwargs.get('z')
            assert len(self.x) == len(self.y) == len(self.z),\
                f'Coordinates have different lengths: ({len(self.x)}, {len(self.y)}, {len(self.z)})'

        else:
            raise KeyError(f'Must pass [x, y, z] as kwargs, got {list(kwargs.keys())}.')

        self.name = kwargs.get('name', 'PLACEHOLDER_NAME')
        self.ext = kwargs.get('ext', 'PLACEHOLDER_EXT')

    def get_vertices(self) -> np.ndarray:
        return np.array(list(zip(self.x, self.y, self.z)), np.float32)

    @staticmethod
    def flatten(l):
        return [item for sublist in l for item in sublist]

    @staticmethod
    def average_by_coord(array: np.array) -> list:
        # Given: [[x1, y1, z1], [x2, y2, z2], [x3, y3, z3]]
        # Expected: [mean([x1, x2, x3]), mean([y1, y2, y3]), mean([z1, z2, z3])]
        return list(map(mean, zip(*array.tolist())))
