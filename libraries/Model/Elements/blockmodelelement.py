#!/usr/bin/env python

import numpy as np
from .element import Element


class BlockModelElement(Element):
    def __init__(self, *args, **kwargs):
        self._data: dict = None
        self._values: np.ndarray = np.array([], np.float32)
        self._size = None

        self._x_str: str = None
        self._y_str: str = None
        self._z_str: str = None
        self._value_str: str = None

        super().__init__(*args, **kwargs)

    def _fill_element(self, *args, **kwargs):
        msg = f'Must pass ["x", "y", "z", "values"], ["vertices", "values"] or ["data"] ' \
            f'as kwargs, got {list(kwargs.keys())}.'

        if 'values' in kwargs.keys():
            super()._fill_element(msg, *args, **kwargs)
            self._fill_as_values(msg, *args, **kwargs)
        elif 'data' in kwargs.keys():
            self._fill_as_data(msg, *args, **kwargs)
        else:
            raise KeyError(msg)

        self._fill_size(*args, **kwargs)

    def _fill_size(self, *args, **kwargs):
        self.block_size = kwargs.get('block_size', [1.0, 1.0, 1.0])

    def _fill_as_values(self, *args, **kwargs):
        self.values = kwargs.get('values')
        self.x_str, self.y_str, self.z_str, self.value_str = 'x', 'y', 'z', 'values'

        self._check_integrity()

    def _fill_as_data(self, *args, **kwargs):
        msg = '"data" cannot be empty.'
        self.data = kwargs.get('data')

        assert len(self.data) > 0, msg

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
    def available_value_names(self) -> list:
        return list(self._data.keys())

    @available_value_names.setter
    def available_value_names(self, values: list) -> None:
        self.x_str, self.y_str, self.z_str, self.value_str = values

    @property
    def block_size(self):
        return self._size

    @block_size.setter
    def block_size(self, size) -> None:
        self._size = np.array(size, np.float32)

    def update_values(self):
        self.x = self.data[self.x_str]
        self.y = self.data[self.y_str]
        self.z = self.data[self.z_str]
        self.values = self.data[self.value_str]
