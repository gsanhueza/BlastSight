#!/usr/bin/env python

import numpy as np


class Element:
    def __init__(self, *args, **kwargs):
        # Base data
        self._data: dict = {}
        self.x_str: str = 'x'
        self.y_str: str = 'y'
        self.z_str: str = 'z'
        self.value_str: str = 'values'

        # Metadata
        self._id: int = None
        self._properties: dict = None

        self._fill_element(*args, **kwargs)
        self._fill_metadata(*args, **kwargs)

    def __del__(self):
        self._data.clear()
        self._properties.clear()

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
        for k in ['x', 'y', 'z', 'vertices', 'indices', 'data']:
            if k in kwargs.keys():
                del kwargs[k]

        self._properties = kwargs

    def _fill_as_vertices(self, msg, *args, **kwargs):
        assert 'vertices' in kwargs.keys(), msg

        self.vertices = np.array(kwargs.get('vertices', []), np.float32)

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
    def x(self):
        return self.data.get(self.x_str, np.empty(0))

    @x.setter
    def x(self, val):
        self.data[self.x_str] = np.array(val, np.float32)

    @property
    def y(self):
        return self.data.get(self.y_str, np.empty(0))

    @y.setter
    def y(self, val):
        self.data[self.y_str] = np.array(val, np.float32)

    @property
    def z(self):
        return self.data.get(self.z_str, np.empty(0))

    @z.setter
    def z(self, val):
        self.data[self.z_str] = np.array(val, np.float32)

    @property
    def vertices(self) -> np.ndarray:
        return np.column_stack((self.x, self.y, self.z))

    @vertices.setter
    def vertices(self, vertices: list) -> None:
        self.x, self.y, self.z = np.array(vertices, np.float32).T

    @property
    def values(self) -> np.ndarray:
        return self.data.get(self.value_str, np.empty(0))

    @values.setter
    def values(self, val):
        self.data[self.value_str] = np.array(val, np.float32)

    @property
    def data(self) -> dict:
        return self._data

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, _id: int) -> None:
        self._id = _id

    @property
    def centroid(self) -> np.ndarray:
        return np.array([self.x.mean(), self.y.mean(), self.z.mean()])

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
