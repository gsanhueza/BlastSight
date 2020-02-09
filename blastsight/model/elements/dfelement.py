#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np
import pandas as pd

from .element import Element
from ...model import utils


class DFElement(Element):
    __slots__ = ['_mapper', '_datasets']

    def __init__(self, *args, **kwargs):
        """
        DFElement (DataFrameElement) is a class designed with the following idea:
        (replace list for numpy arrays in the implementation)

        {
            'data': {
                'x': list[float],
                'y': list[float],
                'z': list[float],
                'values: list[float],
            },
            'datasets': {
                'color': list[list[float]] (Optional, auto-generated from 'values' if None)
            },
            'properties': {
                'headers': list[str],
                'vmin': float,
                'vmax': float,
                'alpha': float,
                'colormap': str (Optional, used from 'values')
            }
            'metadata': {
                'id': int,
                'name': str or None,
                'extension': str or None
            }
        }

        The 'data' dictionary has at least 4 keys, but it can be more than 4.
        It will be implemented as a Pandas DataFrame.
        They don't need to be named 'x, y, z, values' (see self.mapper).

        The 'datasets' dictionary was created because some properties
        might get too big to fit in an HDF5 attribute.
        It's expected to be used by children of this class.
        """
        # Base data
        self._data: pd.DataFrame = pd.DataFrame()
        self._datasets: dict = {}
        self._properties: dict = {}
        self._metadata: dict = {'id': -1}

        self._mapper: dict = {k: k for k in ['x', 'y', 'z', 'values']}
        super()._initialize(*args, **kwargs)

    """
    Element filling
    """
    def _fill_element(self, *args, **kwargs) -> None:
        # Base data
        msg = f'Data must contain ["x", "y", "z"], "vertices" or "data", got {list(kwargs.keys())}.'
        if 'data' in kwargs.keys():
            self._fill_as_data(*args, **kwargs)
        elif 'vertices' in kwargs.keys():
            self._fill_as_vertices(*args, **kwargs)
            self._fill_as_values(*args, **kwargs)
        elif 'x' in kwargs.keys() and 'y' in kwargs.keys() and 'z' in kwargs.keys():
            self._fill_as_xyz(*args, **kwargs)
            self._fill_as_values(*args, **kwargs)
        else:
            raise KeyError(msg)

    def _fill_as_values(self, *args, **kwargs) -> None:
        self.values = np.array(kwargs.get('values', np.empty(self.x.size)))

    def _fill_as_data(self, *args, **kwargs) -> None:
        self.data = kwargs.get('data')

    def _fill_properties(self, *args, **kwargs) -> None:
        self.headers = kwargs.get('headers', list(self.data.keys())[:4])
        self.alpha = kwargs.get('alpha', 1.0)
        self.colormap = kwargs.get('colormap', 'red-blue')  # red-blue (min is red, max is blue)
        self.color = kwargs.get('color', [])

        self.vmin = kwargs.get('vmin', self.values.min())
        self.vmax = kwargs.get('vmax', self.values.max())

    """
    Main accessors (Override)
    """
    @property
    def data(self) -> pd.DataFrame:
        return self._data

    @data.setter
    def data(self, _data: dict) -> None:
        self._data = pd.DataFrame(_data)

    @property
    def mapper(self) -> dict:
        return self._mapper

    @property
    def datasets(self) -> dict:
        return self._datasets

    """
    Data
    """
    @property
    def x(self) -> np.ndarray:
        return self.data[self.mapper.get('x')].to_numpy()

    @property
    def y(self) -> np.ndarray:
        return self.data[self.mapper.get('y')].to_numpy()

    @property
    def z(self) -> np.ndarray:
        return self.data[self.mapper.get('z')].to_numpy()

    @property
    def values(self) -> np.ndarray:
        return self.data[self.mapper.get('values')].to_numpy()

    @x.setter
    def x(self, _x: list) -> None:
        self.data[self.mapper.get('x')] = np.array(_x)

    @y.setter
    def y(self, _y: list) -> None:
        self.data[self.mapper.get('y')] = np.array(_y)

    @z.setter
    def z(self, _z: list) -> None:
        self.data[self.mapper.get('z')] = np.array(_z)

    @values.setter
    def values(self, _values) -> None:
        self.data[self.mapper.get('values')] = np.array(_values)

    """
    Properties
    """
    @property
    def color(self) -> np.ndarray:
        if self.datasets.get('color').size == 0:
            return utils.values_to_rgb(self.values, self.vmin, self.vmax, self.colormap)
        return self.datasets.get('color')

    @property
    def colormap(self) -> str:
        return self.properties.get('colormap')

    @property
    def vmin(self) -> float:
        return self.properties.get('vmin')

    @property
    def vmax(self) -> float:
        return self.properties.get('vmax')

    @color.setter
    def color(self, _colors: list) -> None:
        self.datasets['color'] = np.array(_colors)

    @property
    def all_headers(self) -> list:
        return list(self.data.keys())

    @property
    def headers(self) -> list:
        return list(self.mapper.values())

    @colormap.setter
    def colormap(self, _colormap: str) -> None:
        if utils.parse_colormap(_colormap):  # Empty list interpreted as False
            self.properties['colormap'] = _colormap

    @vmin.setter
    def vmin(self, _vmin: float) -> None:
        try:
            self.properties['vmin'] = float(_vmin)
        except Exception:
            self.properties['vmin'] = self.values.min()

    @vmax.setter
    def vmax(self, _vmax: float) -> None:
        try:
            self.properties['vmax'] = float(_vmax)
        except Exception:
            self.properties['vmax'] = self.values.max()

    @headers.setter
    def headers(self, _headers: list) -> None:
        self.mapper['x'], self.mapper['y'], self.mapper['z'], self.mapper['values'] = _headers
