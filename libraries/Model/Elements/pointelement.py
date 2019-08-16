#!/usr/bin/env python

import numpy as np
from .element import Element


class PointElement(Element):
    def __init__(self, *args, **kwargs):
        self._size = []
        self.colormap = 'redblue'  # redblue (min is red) or bluered (min is blue)
        self.vmin = 0.0
        self.vmax = 1.0

        super().__init__(*args, **kwargs)

    def _fill_element(self, *args, **kwargs):
        msg = f'Must pass ["x", "y", "z", "color"], ["vertices", "color"] or ["data"] ' \
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
        self.point_size = kwargs.get('point_size', 1.0)

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
    def headers(self) -> list:
        return list(self._dataframe.keys())

    @headers.setter
    def headers(self, values: list) -> None:
        self.x_str, self.y_str, self.z_str, self.value_str = values

    @property
    def point_size(self):
        return self._size

    @point_size.setter
    def point_size(self, size) -> None:
        if type(size) is float:
            self._size = np.tile(size, self.x.size)
        else:
            self._size = np.array(size)

    @property
    def marker(self):
        return self._properties.get('marker', 'circle')

    def update_values(self):
        self.data.clear()
        self.x = self._dataframe[self.x_str]
        self.y = self._dataframe[self.y_str]
        self.z = self._dataframe[self.z_str]
        self.values = self._dataframe[self.value_str]
        self.point_size = 1.0
