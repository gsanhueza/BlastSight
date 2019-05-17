#!/usr/bin/env python

import colorsys
import numpy as np
from Model.Elements.element import Element


class BlockModelElement(Element):
    def __init__(self, *args, **kwargs):
        self._data: dict = None
        self._values: np.ndarray = np.array([], np.float32)
        self._x_str: str = None
        self._y_str: str = None
        self._z_str: str = None
        self._value_str: str = None

        self.x_str = kwargs.get('easting', None)
        self.y_str = kwargs.get('northing', None)
        self.z_str = kwargs.get('elevation', None)
        self.current_str = kwargs.get('value', None)

        super().__init__(*args, **kwargs)

    def _init_fill(self, *args, **kwargs):
        if 'vertices' in kwargs.keys():
            self.x, self.y, self.z = zip(*kwargs.get('vertices'))

        elif all(elem in list(kwargs.keys()) for elem in ['x', 'y', 'z']):
            self.x = kwargs.get('x')
            self.y = kwargs.get('y')
            self.z = kwargs.get('z')
            assert len(self.x) == len(self.y) == len(self.z), \
                f'Coordinates have different lengths: ({len(self.x)}, {len(self.y)}, {len(self.z)})'

        elif 'data' in kwargs.keys():
            self.data = kwargs.get('data')

        else:
            raise KeyError(f'Must pass ["x", "y", "z"], "vertices" or "data" as kwargs, got {list(kwargs.keys())}.')

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

    def get_available_coords(self) -> list:
        if self.x_str is None:
            return list(self.data.keys())

        return sorted([self.x_str, self.y_str, self.z_str])

    def get_available_values(self) -> list:
        available = list(self.data.keys())

        if self.x_str is not None:
            available.remove(self.x_str)
            available.remove(self.y_str)
            available.remove(self.z_str)

        return available

    def update_coords(self):
        self.x = list(map(float, self.data[self.x_str]))
        self.y = list(map(float, self.data[self.y_str]))
        self.z = list(map(float, self.data[self.z_str]))

    def update_values(self):
        values = list(map(float, self.data[self.value_str]))
        min_values = min(values)
        max_values = max(values)

        normalized_values = map(lambda val: BlockModelElement.normalize(val, min_values, max_values), values)
        self.values = list(map(lambda hue: colorsys.hsv_to_rgb(hue, 1.0, 1.0), normalized_values))

    @staticmethod
    def normalize(x: float, min_val: float, max_val: float) -> float:
        return (x - min_val) / (max_val - min_val) if max_val != min_val else 0
