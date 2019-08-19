#!/usr/bin/env python

import numpy as np
import pandas as pd
from .element import Element
from ..utils import hsv_to_rgb


class DFElement(Element):
    __slots__ = ['_mapper']

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
            'properties': {
                'headers': list[str],
                'vmin': float,
                'vmax': float,
                'size': float,
                'alpha': float,
                'colormap': str
                'colors': list[list[float]] (Optional, auto-generated if None)
            }
            'metadata': {
                'id': int,
                'name': str or None,
                'extension': str or None
            }
        }

        Where 'data' will be implemented as a Pandas DataFrame, and has at least 4 keys.
        """
        # Base data
        self._data: pd.DataFrame = pd.DataFrame()
        self._mapper: dict = {'x': 'x', 'y': 'y', 'z': 'z', 'values': 'values'}
        self._properties: dict = {}
        self._metadata: dict = {'id': -1}

        super()._initialize(*args, **kwargs)

    """
    Element filling    
    """
    def _fill_element(self, *args, **kwargs):
        # Base data
        msg = f'Data must contain ["x", "y", "z"]. "vertices" or "data", got {list(kwargs.keys())}.'
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

    def _fill_as_vertices(self, *args, **kwargs):
        self.vertices = kwargs.get('vertices', [])

    def _fill_as_xyz(self, *args, **kwargs):
        self.x = kwargs.get('x', [])
        self.y = kwargs.get('y', [])
        self.z = kwargs.get('z', [])

    def _fill_as_values(self, *args, **kwargs):
        self.values = np.array(kwargs.get('values', np.empty(self.x.size)))

    def _fill_as_data(self, *args, **kwargs):
        self.data = kwargs.get('data')

    def _fill_properties(self, *args, **kwargs):
        self.headers = kwargs.get('headers', list(self.data.keys())[:4])
        self.alpha = kwargs.get('alpha', 1.0)

        try:
            self.vmin = kwargs.get('vmin', self.values.min())
            self.vmax = kwargs.get('vmax', self.values.max())
        except ValueError:
            self.vmin = kwargs.get('vmin', 0.0)
            self.vmax = kwargs.get('vmax', 1.0)

        self._fill_size(*args, **kwargs)

    def _fill_size(self, *args, **kwargs):
        self.size = kwargs.get('size', 1.0)

    def _fill_metadata(self, *args, **kwargs):
        self.name = kwargs.get('name', None)
        self.extension = kwargs.get('ext', None)

    def _check_integrity(self):
        msg = '"data" cannot be empty.'
        if len(self.data) == 0:
            raise ValueError(msg)

        msg = f'Coordinates have different lengths: ({self.x.size}, {self.y.size}, {self.z.size})'
        if not (self.x.size == self.y.size == self.z.size):
            raise ValueError(msg)

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
    def color(self):
        if self.properties.get('color').size == 0:
            return self.values_to_rgb(self.values, self.vmin, self.vmax, self.colormap)
        return self.properties.get('color')

    @property
    def colormap(self) -> str:
        return self.properties.get('colormap')

    @property
    def headers(self) -> list:
        return list(self.data.keys())

    @property
    def vmin(self) -> float:
        return self.properties.get('vmin')

    @property
    def vmax(self) -> float:
        return self.properties.get('vmax')

    @property
    def size(self) -> float:
        return self.properties.get('size')

    @color.setter
    def color(self, _colors: list):
        self.properties['color'] = np.array(_colors)

    @colormap.setter
    def colormap(self, _colormap: str) -> None:
        self.properties['colormap'] = _colormap

    @headers.setter
    def headers(self, _headers: list) -> None:
        self.mapper['x'], self.mapper['y'], self.mapper['z'], self.mapper['values'] = _headers

    @vmin.setter
    def vmin(self, _vmin: float) -> None:
        self.properties['vmin'] = _vmin

    @vmax.setter
    def vmax(self, _vmax: float) -> None:
        self.properties['vmax'] = _vmax

    @size.setter
    def size(self, _size: float) -> None:
        self.properties['size'] = _size

    """
    Utilities
    """
    @staticmethod
    def color_from_dict(colormap: str):
        d = {
            'redblue': lambda v: 2.0 / 3.0 * v,
            'bluered': lambda v: 2.0 / 3.0 * (1.0 - v),
        }

        return d.get(colormap)

    @staticmethod
    def values_to_rgb(values: np.ndarray, vmin: float, vmax: float, colormap: str):
        values = np.clip(values, vmin, vmax)
        norm = values.max() - values.min()
        if norm == 0:
            return np.ones(3 * values.size)

        vals = (values - values.min()) / norm
        hsv = np.ones((vals.size, 3))

        hsv[:, 0] = DFElement.color_from_dict(colormap)(vals)
        return hsv_to_rgb(hsv)

    """
    Mapper handling
    """
    @property
    def x_str(self) -> str:
        return self.mapper.get('x')

    @property
    def y_str(self) -> str:
        return self.mapper.get('y')

    @property
    def z_str(self) -> str:
        return self.mapper.get('z')

    @property
    def value_str(self) -> str:
        return self.mapper.get('values')

    @x_str.setter
    def x_str(self, _x_str: str) -> None:
        self.mapper['x'] = _x_str

    @y_str.setter
    def y_str(self, _y_str: str) -> None:
        self.mapper['y'] = _y_str

    @z_str.setter
    def z_str(self, _z_str: str) -> None:
        self.mapper['z'] = _z_str

    @value_str.setter
    def value_str(self, _value_str: str) -> None:
        self.mapper['values'] = _value_str
