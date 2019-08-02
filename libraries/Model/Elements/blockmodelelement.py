#!/usr/bin/env python

import numpy as np
from .element import Element


class BlockModelElement(Element):
    def __init__(self, *args, **kwargs):
        self._dataframe = None
        self._size = None

        self.value_str: str = 'values'
        self.vmin = 0.0
        self.vmax = 1.0

        super().__init__(*args, **kwargs)

    @property
    def values(self) -> np.ndarray:
        return self.data.get(self.value_str, np.empty(0))

    @values.setter
    def values(self, val):
        self.data[self.value_str] = np.array(val, np.float32)

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
        self.values = np.array(kwargs.get('values', []), np.float32)
        self.vmin = kwargs.get('vmin', self.values.min())
        self.vmax = kwargs.get('vmax', self.values.max())

        self._check_integrity()

    def _fill_as_data(self, *args, **kwargs):
        msg = '"data" cannot be empty.'
        self._dataframe = kwargs.get('data')

        assert len(self._dataframe) > 0, msg

    @property
    def available_headers(self) -> list:
        return list(self._dataframe.keys())

    @available_headers.setter
    def available_headers(self, values: list) -> None:
        self.x_str, self.y_str, self.z_str, self.value_str = values

    @property
    def block_size(self):
        return self._size

    @block_size.setter
    def block_size(self, size) -> None:
        self._size = np.array(size, np.float32)

    def update_values(self):
        self._data.clear()
        self.x = self._dataframe[self.x_str]
        self.y = self._dataframe[self.y_str]
        self.z = self._dataframe[self.z_str]
        self.values = self._dataframe[self.value_str]
