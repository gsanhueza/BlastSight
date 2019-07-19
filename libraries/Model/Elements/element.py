#!/usr/bin/env python

import numpy as np


class Element:
    def __init__(self, *args, **kwargs):
        # Base data
        self._x: np.ndarray = np.empty(0, np.float32)
        self._y: np.ndarray = np.empty(0, np.float32)
        self._z: np.ndarray = np.empty(0, np.float32)

        # Metadata
        self._id: int = None
        self._properties: dict = None

        self._fill_element(*args, **kwargs)
        self._fill_metadata(*args, **kwargs)

    def _fill_element(self, msg=None, *args, **kwargs):
        if msg is None:
            msg = f'Must pass ["x", "y", "z"] or "vertices" as kwargs, got {list(kwargs.keys())}.'

        if 'vertices' in kwargs.keys():
            self._fill_as_vertices(msg, *args, **kwargs)
        elif 'x' in kwargs.keys() and 'y' in kwargs.keys() and 'z' in kwargs.keys():
            self._fill_as_xyz(msg, *args, **kwargs)
        else:
            raise KeyError(msg)

        self._check_integrity()

    def _fill_metadata(self, *args, **kwargs):
        for k in ['x', 'y', 'z', 'vertices', 'indices']:
            if k in kwargs.keys():
                del kwargs[k]

        self._properties = kwargs

    def _fill_as_vertices(self, msg, *args, **kwargs):
        assert 'vertices' in kwargs.keys(), msg

        self.vertices = kwargs.get('vertices')

    def _fill_as_xyz(self, msg, *args, **kwargs):
        assert 'x' in kwargs.keys(), msg
        assert 'y' in kwargs.keys(), msg
        assert 'z' in kwargs.keys(), msg

        self.x = kwargs.get('x')
        self.y = kwargs.get('y')
        self.z = kwargs.get('z')

    def _check_integrity(self):
        msg = f'Coordinates have different lengths: ({self.x.size}, {self.y.size}, {self.z.size})'
        assert self.x.size == self.y.size == self.z.size, msg

    """
    Attributes
    """
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
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, _id: int) -> None:
        self._id = _id

    @property
    def vertices(self) -> np.ndarray:
        return np.column_stack((self._x, self._y, self._z))

    @vertices.setter
    def vertices(self, vertices: list) -> None:
        self._x, self._y, self._z = np.array(vertices, np.float32).T

    @property
    def centroid(self) -> np.ndarray:
        return np.array([self._x.mean(), self._y.mean(), self._z.mean()])

    """
    Metadata
    """
    @property
    def name(self) -> str:
        return self._properties.get('name', None)

    @name.setter
    def name(self, name: str) -> None:
        self._properties['name'] = name

    @property
    def ext(self) -> str:
        return self._properties.get('ext', None)

    @ext.setter
    def ext(self, ext: str) -> None:
        self._properties['ext'] = ext

    @property
    def alpha(self):
        return self._properties.get('alpha', 1.0)

    @alpha.setter
    def alpha(self, val):
        self._properties['alpha'] = val
