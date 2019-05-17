#!/usr/bin/env python

import colorsys
import numpy as np
from Model.element import Element


class BlockModelElement(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._data = None
        self._values = []

        self.x_str = kwargs.get('easting', None)
        self.y_str = kwargs.get('northing', None)
        self.z_str = kwargs.get('elevation', None)
        self.current_str = kwargs.get('value', None)

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
        return np.array(self._values, np.float32)

    @values.setter
    def values(self, values: list) -> None:
        self._values = values

    # TODO Force the user to set these strings
    def set_x_string(self, string: str) -> None:
        self.x_str = string

    def set_y_string(self, string: str) -> None:
        self.y_str = string

    def set_z_string(self, string: str) -> None:
        self.z_str = string

    def set_value_string(self, string: str) -> None:
        self.current_str = string

    def get_x_string(self) -> str:
        return self.x_str

    def get_y_string(self) -> str:
        return self.y_str

    def get_z_string(self) -> str:
        return self.z_str

    def get_value_string(self) -> str:
        return self.current_str

    def get_available_coords(self) -> list:
        print('get_available_coords', self.data)
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
        x = list(map(float, self.data[self.x_str]))
        y = list(map(float, self.data[self.y_str]))
        z = list(map(float, self.data[self.z_str]))

        self.vertices = list(zip(x, y, z))

    def update_values(self):
        values = list(map(float, self.data[self.current_str]))
        min_values = min(values)
        max_values = max(values)

        normalized_values = map(lambda val: BlockModelElement.normalize(val, min_values, max_values), values)
        self.values = list(map(lambda hue: colorsys.hsv_to_rgb(hue, 1.0, 1.0), normalized_values))

    @staticmethod
    def normalize(x: float, min_val: float, max_val: float) -> float:
        return (x - min_val) / (max_val - min_val) if max_val != min_val else 0
