#!/usr/bin/env python

import pandas as pd
import numpy as np
from .element import Element


class BlockElement(Element):
    def __init__(self, *args, **kwargs):
        self._dataframe = None
        self._size = None
        self._vmin = 0.0
        self._vmax = 1.0

        super().__init__(*args, **kwargs)

    def _fill_element(self, *args, **kwargs):
        msg = f'Must pass ["x", "y", "z", "values"], ["vertices", "values"] or ["data"] ' \
            f'as kwargs, got {list(kwargs.keys())}.'

        if 'color' in kwargs.keys():
            super()._fill_element(msg, *args, **kwargs)
            self._fill_as_colors(*args, **kwargs)
        elif 'values' in kwargs.keys():
            super()._fill_element(msg, *args, **kwargs)
            self._fill_as_values(*args, **kwargs)
        elif 'data' in kwargs.keys():
            self._fill_as_data(msg, *args, **kwargs)
        else:
            raise KeyError(msg)

        self._fill_size(*args, **kwargs)

    def _fill_size(self, *args, **kwargs):
        self.block_size = kwargs.get('block_size', [1.0, 1.0, 1.0])

    def _fill_as_colors(self, *args, **kwargs):
        self.color = np.array(kwargs.get('color', []))
        self.values = np.empty(0)
        self.vmin = 0.0
        self.vmax = 1.0

    def _fill_as_values(self, *args, **kwargs):
        self.color = np.empty(0)
        self.values = np.array(kwargs.get('values', []))
        self.vmin = kwargs.get('vmin', self.values.min())
        self.vmax = kwargs.get('vmax', self.values.max())
        self.colormap = kwargs.get('colormap', 'redblue')

    def _fill_as_data(self, *args, **kwargs):
        msg = '"data" cannot be empty.'
        self._dataframe = kwargs.get('data')
        self.headers = kwargs.get('headers', list(self._dataframe.keys())[:4])

        assert len(self._dataframe) > 0, msg
        self.update_values()

    """
    Properties
    """
    @property
    def dataframe(self):
        if self._dataframe is None:
            self._dataframe = pd.DataFrame(super().data)
        return self._dataframe

    @property
    def block_count(self):
        return np.array([self.x.size, self.y.size, self.z.size])

    @property
    def block_min(self):
        return np.array([self.x.min(), self.y.min(), self.z.min()])

    @property
    def block_max(self):
        return np.array([self.x.max(), self.y.max(), self.z.max()])

    @property
    def block_size(self):
        return self._size

    @property
    def headers(self) -> list:
        return list(self._dataframe.keys())

    @property
    def vmin(self):
        return self._vmin

    @property
    def vmax(self):
        return self._vmax

    @vmin.setter
    def vmin(self, value):
        self._vmin = value

    @vmax.setter
    def vmax(self, value):
        self._vmax = value

    @headers.setter
    def headers(self, values: list) -> None:
        self.x_str, self.y_str, self.z_str, self.value_str = values

    @block_size.setter
    def block_size(self, size) -> None:
        self._size = np.array(size)

    def update_values(self):
        self.data.clear()
        self.x = self._dataframe[self.x_str]
        self.y = self._dataframe[self.y_str]
        self.z = self._dataframe[self.z_str]
        self.values = self._dataframe[self.value_str]
