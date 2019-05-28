#!/usr/bin/env python

import colorsys
import numpy as np
from Model.Elements.element import Element


class BlockModelElement(Element):
    def __init__(self, *args, **kwargs):
        self._data: dict = None
        self._x_str: str = None
        self._y_str: str = None
        self._z_str: str = None
        self._value_str: str = None
        self._values: np.ndarray = None

        super().__init__(*args, **kwargs)

    def _init_fill(self, *args, **kwargs):
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
        try:
            return sorted([self.x_str, self.y_str, self.z_str])
        except TypeError:
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

    def update_coords(self):
        self.x = np.vectorize(float, otypes=[np.float32])(self.data[self.x_str])
        self.y = np.vectorize(float, otypes=[np.float32])(self.data[self.y_str])
        self.z = np.vectorize(float, otypes=[np.float32])(self.data[self.z_str])

    def update_values(self):
        values = np.vectorize(float, otypes=[np.float32])(self.data[self.value_str])
        min_values = values.min()
        max_values = values.max()

        normalized_values = np.vectorize(lambda val: BlockModelElement.normalize(val, min_values, max_values),
                                         otypes=[np.float32])(values)

        # FIXME colorsys.hsv_to_rgb returns a tuple. but np.vectorize doesn't accept it as tuple
        # self.values = np.vectorize(lambda hue: colorsys.hsv_to_rgb(hue, 1.0, 1.0),
        #                            otypes=[np.float32])(normalized_values)
        self.values = np.array(list(map(lambda hue: colorsys.hsv_to_rgb(hue, 1.0, 1.0), normalized_values)),
                               np.float32)

    @staticmethod
    def normalize(x: float, min_val: float, max_val: float) -> float:
        return (x - min_val) / (max_val - min_val) if max_val != min_val else 0
