#!/usr/bin/env python

import numpy as np


class Element:
    def __init__(self, *args, **kwargs):
        # Base data
        self.data: dict = {}
        self.x_str: str = 'x'
        self.y_str: str = 'y'
        self.z_str: str = 'z'
        self.value_str: str = 'values'

        # Metadata
        self._id: int = -1
        self._metadata: dict = {}
        self._properties: dict = {}

        self._fill_element(*args, **kwargs)
        self._fill_metadata(*args, **kwargs)
        self._fill_properties(*args, **kwargs)

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

    def _fill_as_vertices(self, msg, *args, **kwargs):
        assert 'vertices' in kwargs.keys(), msg

        self.vertices = kwargs.get('vertices', [])

    def _fill_as_xyz(self, msg, *args, **kwargs):
        assert 'x' in kwargs.keys(), msg
        assert 'y' in kwargs.keys(), msg
        assert 'z' in kwargs.keys(), msg

        self.x = kwargs.get('x')
        self.y = kwargs.get('y')
        self.z = kwargs.get('z')

    def _fill_metadata(self, *args, **kwargs):
        self._metadata['name'] = kwargs.get('name')
        self._metadata['ext'] = kwargs.get('ext')

        self._metadata = kwargs

    def _fill_properties(self, *args, **kwargs):
        for k in ['x', 'y', 'z', 'vertices', 'values', 'data', 'name', 'ext']:
            if k in kwargs.keys():
                del kwargs[k]

        self._properties = kwargs

    def _check_integrity(self):
        msg = f'Coordinates have different lengths: ({self.x.size}, {self.y.size}, {self.z.size})'
        assert self.x.size == self.y.size == self.z.size, msg

    """
    Attributes
    """
    @property
    def x(self):
        return self.data.get(self.x_str, np.empty(0))

    @property
    def y(self):
        return self.data.get(self.y_str, np.empty(0))

    @property
    def z(self):
        return self.data.get(self.z_str, np.empty(0))

    @property
    def vertices(self) -> np.ndarray:
        return np.column_stack((self.x, self.y, self.z))

    """
    Setters
    """
    @x.setter
    def x(self, val):
        self.data[self.x_str] = np.array(val, np.float32)

    @y.setter
    def y(self, val):
        self.data[self.y_str] = np.array(val, np.float32)

    @z.setter
    def z(self, val):
        self.data[self.z_str] = np.array(val, np.float32)

    @vertices.setter
    def vertices(self, vertices: list) -> None:
        self.x, self.y, self.z = np.array(vertices).T

    @property
    def centroid(self) -> np.ndarray:
        return np.array([self.x.mean(), self.y.mean(), self.z.mean()])

    """
    Metadata
    """
    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, _id: int) -> None:
        self._id = _id

    @property
    def name(self) -> str:
        return self._metadata.get('name', None)

    @name.setter
    def name(self, name: str) -> None:
        self._metadata['name'] = name

    @property
    def ext(self) -> str:
        return self._metadata.get('ext', None)

    @ext.setter
    def ext(self, ext: str) -> None:
        self._metadata['ext'] = ext

    @property
    def color(self) -> np.array:
        return self.data.get('color', np.ones(3))

    @color.setter
    def color(self, val):
        self.data['color'] = np.array(val)

    @property
    def alpha(self):
        return self.data.get('alpha', 1.0)

    @alpha.setter
    def alpha(self, val):
        self.data['alpha'] = val

    @property
    def rgba(self):
        return np.array(np.append(self.color, self.alpha))
