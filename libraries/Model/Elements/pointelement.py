#!/usr/bin/env python

import numpy as np
from multiprocess import Pool
from .element import Element


class PointElement(Element):
    def __init__(self, *args, **kwargs):
        self._data: dict = None
        self._x_str: str = None
        self._y_str: str = None
        self._z_str: str = None
        self._value_str: str = None
        self._values: np.ndarray = None
        self._point_size: float = 10.0

        super().__init__(*args, **kwargs)

    def _init_fill(self, *args, **kwargs):
        msg = f'Must pass ["x", "y", "z", "values"], ["vertices", "values"] or ["data"] ' \
            f'as kwargs, got {list(kwargs.keys())}.'

        if 'values' in kwargs.keys():
            self._fill_as_values(msg, *args, **kwargs)
        elif 'data' in kwargs.keys():
            self._fill_as_data(msg, *args, **kwargs)
        else:
            raise KeyError(msg)

        self.name = kwargs.get('name', None)
        self.ext = kwargs.get('ext', None)
        self.alpha = kwargs.get('alpha', 1.0)
        self.block_size = kwargs.get('point_size', 1.0)

    def _fill_as_values(self, msg, *args, **kwargs):
        assert len(kwargs.keys()) >= 2

        if 'vertices' in kwargs.keys():
            super()._fill_as_vertices(msg, *args, **kwargs)
        else:
            super()._fill_as_xyz(msg, *args, **kwargs)

        self.values = kwargs.get('values')
        self.x_str, self.y_str, self.z_str, self.value_str = 'x', 'y', 'z', 'values'

        self._check_integrity()

    def _fill_as_data(self, msg, *args, **kwargs):
        self.data = kwargs.get('data')

        assert len(self.data) > 0, msg

    def _check_integrity(self):
        super()._check_integrity()
        assert len(self.x) == len(self.values)

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
    def point_size(self) -> float:
        return self._point_size

    @point_size.setter
    def point_size(self, size: float) -> None:
        self._point_size = size

    def update_values(self):
        with Pool(processes=4) as pool:
            self.x, self.y, self.z, self.values = pool.map(np.float32, [
                self.data[self.x_str],
                self.data[self.y_str],
                self.data[self.z_str],
                self.data[self.value_str],
            ])
