#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np


class Element:
    __slots__ = ['data', 'properties', 'metadata']

    def __init__(self, *args, **kwargs):
        """
        Element is a class designed with the following idea:
        (replace list for numpy arrays in the implementation)

        {
            'data': {
                'x': list[float],
                'y': list[float],
                'z': list[float]
            }
            'properties': {
                'color': list[float],
                'alpha': float
            },
            'metadata': {
                'id': int,
                'name': str,
                'extension': str
            }
        }
        """
        # Base data
        self.data: dict = {}
        self.properties: dict = {}
        self.metadata: dict = {}

        self._initialize(*args, **kwargs)

    def _initialize(self, *args, **kwargs) -> None:
        self._fill_element(*args, **kwargs)
        self._fill_metadata(*args, **kwargs)
        self._fill_properties(*args, **kwargs)
        self._check_integrity()

    """
    Element filling
    """
    def _fill_element(self, *args, **kwargs) -> None:
        msg = f'Data must contain ["x", "y", "z"], "vertices" or "data", got {list(kwargs.keys())}.'
        if 'data' in kwargs.keys():
            self._fill_as_data(*args, **kwargs)
        elif 'vertices' in kwargs.keys():
            self._fill_as_vertices(*args, **kwargs)
        elif 'x' in kwargs.keys() and 'y' in kwargs.keys() and 'z' in kwargs.keys():
            self._fill_as_xyz(*args, **kwargs)
        else:
            raise KeyError(msg)

    def _fill_as_data(self, *args, **kwargs) -> None:
        data = kwargs.get('data', {})
        if 'vertices' in data.keys():
            self.vertices = data.get('vertices', [])
        else:
            self.x = data.get('x', [])
            self.y = data.get('y', [])
            self.z = data.get('z', [])

    def _fill_as_vertices(self, *args, **kwargs) -> None:
        self.vertices = kwargs.get('vertices', [])

    def _fill_as_xyz(self, *args, **kwargs) -> None:
        self.x = kwargs.get('x', [])
        self.y = kwargs.get('y', [])
        self.z = kwargs.get('z', [])

    def _fill_properties(self, *args, **kwargs) -> None:
        self.color = kwargs.get('color', np.random.rand(3))
        self.alpha = kwargs.get('alpha', 1.0)

    def _fill_metadata(self, *args, **kwargs) -> None:
        self.name = kwargs.get('name')
        self.extension = kwargs.get('extension')
        self.id = kwargs.get('id', -1)

    def _check_integrity(self) -> None:
        msg = f'Coordinates have different lengths: ({self.x.size}, {self.y.size}, {self.z.size})'
        if not (self.x.size == self.y.size == self.z.size):
            raise ValueError(msg)

    """
    Dynamic properties (custom properties set by the user)
    """
    def __dir__(self) -> list:
        # We need both our methods/attributes, and the keys of the _properties dict
        return list(set(super().__dir__() + list(self.properties.keys())))

    def __getattribute__(self, attr: str):
        # Do we have the desired attribute/property?
        if hasattr(type(self), attr):
            return super().__getattribute__(attr)

        # Does self.properties have it?
        if attr in super().__getattribute__('properties').keys():
            return super().__getattribute__('properties')[attr]

        # If everything fails, just raise the original exception
        return super().__getattribute__(attr)

    """
    Properties accessors
    """
    def set_property(self, key: str, value: any) -> None:
        self.properties[key] = value

    def get_property(self, key: str, default: any = None) -> any:
        return self.properties.get(key, default)

    def delete_property(self, key: str) -> None:
        self.properties.pop(key)

    """
    Data accessors
    """
    @property
    def x(self) -> np.ndarray:
        return self.data.get('x')

    @property
    def y(self) -> np.ndarray:
        return self.data.get('y')

    @property
    def z(self) -> np.ndarray:
        return self.data.get('z')

    @property
    def vertices(self) -> np.ndarray:
        return np.column_stack((self.x, self.y, self.z))

    @x.setter
    def x(self, val: list) -> None:
        self.data['x'] = np.array(val, np.float32)

    @y.setter
    def y(self, val: list) -> None:
        self.data['y'] = np.array(val, np.float32)

    @z.setter
    def z(self, val: list) -> None:
        self.data['z'] = np.array(val, np.float32)

    @vertices.setter
    def vertices(self, vertex_list: list) -> None:
        self.x, self.y, self.z = np.array(vertex_list).T

    """
    Properties
    """
    @property
    def attributes(self) -> dict:
        return {**self.properties, **self.metadata}

    @property
    def color(self) -> np.array:
        return self.properties.get('color')

    @property
    def alpha(self) -> float:
        return self.properties.get('alpha')

    @property
    def rgba(self) -> np.ndarray:
        return np.append(self.color, self.alpha)

    @color.setter
    def color(self, val: list) -> None:
        self.properties['color'] = np.array(val)

    @alpha.setter
    def alpha(self, val: float) -> None:
        self.properties['alpha'] = val

    @rgba.setter
    def rgba(self, val: list) -> None:
        self.color = np.array(val)[:3]
        self.alpha = val[-1]

    """
    Utilities
    """
    @property
    def centroid(self) -> np.ndarray:
        return self.vertices.mean(axis=0)

    @property
    def center(self) -> np.ndarray:
        return np.sum(self.bounding_box, axis=0) / 2

    @property
    def bounding_box(self) -> tuple:
        # We could return self.vertices.min(axis=0), self.vertices.max(axis=0),
        # but I found this to be noticeable faster (speedup of 5.2 approx.)
        return (np.array([self.x.min(), self.y.min(), self.z.min()]),
                np.array([self.x.max(), self.y.max(), self.z.max()]))

    """
    Metadata
    """
    @property
    def id(self) -> int:
        return self.metadata.get('id')

    @property
    def name(self) -> str:
        return self.metadata.get('name')

    @property
    def extension(self) -> str:
        return self.metadata.get('extension')

    @id.setter
    def id(self, _id: int) -> None:
        self.metadata['id'] = _id

    @name.setter
    def name(self, _name: str) -> None:
        self.metadata['name'] = _name

    @extension.setter
    def extension(self, _extension: str) -> None:
        self.metadata['extension'] = _extension
