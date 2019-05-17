#!/usr/bin/env python

import numpy as np
from statistics import mean


class Element:
    def __init__(self, *args, **kwargs):
        self._x = []
        self._y = []
        self._z = []
        self._centroid = []
        self._name = None
        self._ext = None

        self._init_fill(*args, **kwargs)

    def _init_fill(self, *args, **kwargs):
        if 'vertices' in kwargs.keys():
            self.x, self.y, self.z = zip(*kwargs.get('vertices'))

        elif all(elem in list(kwargs.keys()) for elem in ['x', 'y', 'z']):
            self.x = kwargs.get('x')
            self.y = kwargs.get('y')
            self.z = kwargs.get('z')

            assert len(self.x) == len(self.y) == len(self.z),\
                f'Coordinates have different lengths: ({len(self.x)}, {len(self.y)}, {len(self.z)})'

        else:
            raise KeyError(f'Must pass ["x", "y", "z"] or "vertices" as kwargs, got {list(kwargs.keys())}.')

        self.name = kwargs.get('name', None)
        self.ext = kwargs.get('ext', None)

    @property
    def x(self) -> list:
        return self._x

    @property
    def y(self) -> list:
        return self._y

    @property
    def z(self) -> list:
        return self._z

    @property
    def name(self) -> list:
        return self._name

    @property
    def ext(self) -> list:
        return self._ext

    @property
    def vertices(self) -> np.ndarray:
        return np.array(list(zip(self._x, self._y, self._z)), np.float32)

    @property
    def centroid(self) -> np.ndarray:
        return np.array(Element.average_by_coord(self.vertices))

    @x.setter
    def x(self, x) -> None:
        self._x = x

    @y.setter
    def y(self, y) -> None:
        self._y = y

    @z.setter
    def z(self, z) -> None:
        self._z = z

    @name.setter
    def name(self, name) -> None:
        self._name = name

    @ext.setter
    def ext(self, ext) -> None:
        self._ext = ext

    @vertices.setter
    def vertices(self, vertices: list) -> None:
        self._x, self._y, self._z = zip(*vertices)
        self._centroid = Element.average_by_coord(self.vertices)

    @staticmethod
    def flatten(l):
        return [item for sublist in l for item in sublist]

    @staticmethod
    def average_by_coord(array: np.array) -> list:
        # Given: [[x1, y1, z1], [x2, y2, z2], [x3, y3, z3]]
        # Expected: [mean([x1, x2, x3]), mean([y1, y2, y3]), mean([z1, z2, z3])]
        return list(map(mean, zip(*array.tolist())))
