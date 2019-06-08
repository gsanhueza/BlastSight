#!/usr/bin/env python

import numpy as np
from multiprocess import Pool
from .element import Element


class BlockModelElement(Element):
    def __init__(self, *args, **kwargs):
        self._data: dict = None
        self._x_str: str = None
        self._y_str: str = None
        self._z_str: str = None
        self._value_str: str = None
        self._values: np.ndarray = None
        self._block_size: np.ndarray = None

        super().__init__(*args, **kwargs)

    def _init_fill(self, *args, **kwargs):
        self.block_size = kwargs.get('block_size', [1.0, 1.0, 1.0])

        if all(elem in list(kwargs.keys()) for elem in ['vertices', 'values']):
            assert len(kwargs.keys()) >= 2

            self.x, self.y, self.z = zip(*kwargs.get('vertices'))
            self.values = kwargs.get('values')

            assert len(self.x) == len(self.y) == len(self.z) == len(self.values), \
                f'Coordinates have different lengths: ({len(self.x)}, {len(self.y)}, {len(self.z)}, {len(self.values)})'

            self.x_str, self.y_str, self.z_str, self.value_str = ['x', 'y', 'z', 'values']

        elif all(elem in list(kwargs.keys()) for elem in ['x', 'y', 'z', 'values']):
            assert len(kwargs.keys()) >= 4

            self.x = kwargs.get('x')
            self.y = kwargs.get('y')
            self.z = kwargs.get('z')
            self.values = kwargs.get('values')

            assert len(self.x) == len(self.y) == len(self.z) == len(self.values), \
                f'Coordinates have different lengths: ({len(self.x)}, {len(self.y)}, {len(self.z)}, {len(self.values)})'

            self.x_str, self.y_str, self.z_str, self.value_str = ['x', 'y', 'z', 'values']

        elif all(elem in list(kwargs.keys()) for elem in ['data']):
            self.data = kwargs.get('data')
            self.values = []

            assert len(self.data) >= 4

        else:
            raise KeyError(f'Must pass ["x", "y", "z", "values"], ["vertices", "values"] or ["data"] '
                           f'as kwargs, got {list(kwargs.keys())}.')

        self.name = kwargs.get('name', None)
        self.ext = kwargs.get('ext', None)

    @property
    def data(self) -> dict:
        return self._data

    @data.setter
    def data(self, data: dict) -> None:
        self._data = data

    @property
    def values(self) -> np.ndarray:
        return self._values

    @values.setter
    def values(self, values: list):
        self._values = np.array(values, np.float32)

    @property
    def x_str(self) -> str:
        return self._x_str

    @x_str.setter
    def x_str(self, x_str: str) -> None:
        self._x_str = x_str

    @property
    def y_str(self) -> str:
        return self._y_str

    @y_str.setter
    def y_str(self, y_str: str) -> None:
        self._y_str = y_str

    @property
    def z_str(self) -> str:
        return self._z_str

    @z_str.setter
    def z_str(self, z_str: str) -> None:
        self._z_str = z_str

    @property
    def value_str(self) -> str:
        return self._value_str

    @value_str.setter
    def value_str(self, value_str: str) -> None:
        self._value_str = value_str

    @property
    def available_coordinates(self) -> list:
        if self.x_str and self.y_str and self.z_str:
            return sorted([self.x_str, self.y_str, self.z_str])
        else:
            return list(self.data.keys())

    @available_coordinates.setter
    def available_coordinates(self, available: list) -> None:
        self._x_str, self._y_str, self._z_str = available

    @property
    def available_values(self) -> list:
        available = list(self._data.keys())

        if self.x_str is not None:
            available.remove(self.x_str)
        if self.y_str is not None:
            available.remove(self.y_str)
        if self.z_str is not None:
            available.remove(self.z_str)

        return available

    @property
    def block_size(self) -> np.ndarray:
        return self._block_size

    @block_size.setter
    def block_size(self, size: list) -> None:
        self._block_size = np.array(size, np.float32)

    def update_coords(self):
        with Pool(processes=3) as pool:
            self.x, self.y, self.z = pool.map(np.float32, [
                self.data[self.x_str],
                self.data[self.y_str],
                self.data[self.z_str],
            ])

    def update_values(self):
        self.values = list(map(np.float32, self.data[self.value_str]))
