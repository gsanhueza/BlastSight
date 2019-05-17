#!/usr/bin/env python

import numpy as np


class Element:
    def __init__(self, *args, **kwargs):
        self._x: np.ndarray = np.array([], np.float32)
        self._y: np.ndarray = np.array([], np.float32)
        self._z: np.ndarray = np.array([], np.float32)
        self._name: str = None
        self._ext: str = None

        self._init_fill(*args, **kwargs)

    def _init_fill(self, *args, **kwargs):
        if 'vertices' in kwargs.keys():
            self.x, self.y, self.z = zip(*kwargs.get('vertices'))

        elif all(elem in list(kwargs.keys()) for elem in ['x', 'y', 'z']):
            self.x, self.y, self.z = list(map(lambda s: kwargs.get(s), ['x', 'y', 'z']))

            assert len(self.x) == len(self.y) == len(self.z),\
                f'Coordinates have different lengths: ({self.x.size}, {self.y.size}, {self.z.size})'

        else:
            raise KeyError(f'Must pass ["x", "y", "z"] or "vertices" as kwargs, got {list(kwargs.keys())}.')

        self.name = kwargs.get('name', None)
        self.ext = kwargs.get('ext', None)

    @property
    def x(self) -> np.ndarray:
        return self._x

    @x.setter
    def x(self, x: list) -> None:
        self._x = np.array(x, np.float32)

    @property
    def y(self) -> np.ndarray:
        return self._y

    @y.setter
    def y(self, y: list) -> None:
        self._y = np.array(y, np.float32)

    @property
    def z(self) -> np.ndarray:
        return self._z

    @z.setter
    def z(self, z: list) -> None:
        self._z = np.array(z, np.float32)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def ext(self) -> str:
        return self._ext

    @ext.setter
    def ext(self, ext: str) -> None:
        self._ext = ext

    @property
    def vertices(self) -> np.ndarray:
        return np.array(list(zip(self._x, self._y, self._z)), np.float32)

    @vertices.setter
    def vertices(self, vertices: list) -> None:
        x, y, z = zip(*vertices)
        self._x = np.array(x, np.float32)
        self._y = np.array(x, np.float32)
        self._z = np.array(x, np.float32)

    @property
    def centroid(self) -> np.ndarray:
        return np.array(Element.average_by_coord(self._x, self._y, self._z))

    @staticmethod
    def flatten(l: list) -> list:
        return [item for sublist in l for item in sublist]

    @staticmethod
    def average_by_coord(x: np.array, y: np.array, z: np.array) -> np.array:
        # Given: [[x1, y1, z1], [x2, y2, z2], [x3, y3, z3]]
        # Expected: [mean([x1, x2, x3]), mean([y1, y2, y3]), mean([z1, z2, z3])]
        return np.array([x.mean(), y.mean(), z.mean()], np.float32)
