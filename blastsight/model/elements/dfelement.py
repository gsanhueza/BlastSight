#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np
import pandas as pd

from .element import Element
from ...model import utils


class DFElement(Element):
    __slots__ = ['_mapper', 'datasets']

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
        They don't need to be named 'x, y, z, values' (see self._mapper).

        The 'datasets' dictionary was created because some properties
        might get too big to fit in an HDF5 attribute.
        It's expected to be used by children of this class.
        """
        # Base data
        self.data: pd.DataFrame = pd.DataFrame()
        self.datasets: dict = {}
        self.properties: dict = {}
        self.metadata: dict = {'id': -1}

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
        self.data = pd.DataFrame(kwargs.get('data'))

    def _fill_properties(self, *args, **kwargs) -> None:
        self.headers = kwargs.get('headers', list(self.data.keys())[:4])
        self.alpha = kwargs.get('alpha', 1.0)
        self.colormap = kwargs.get('colormap', 'red-blue')  # red-blue (min is red, max is blue)
        self.color = kwargs.get('color', [])
        self.is_slice = kwargs.get('is_slice', False)

        self.vmin = kwargs.get('vmin', self.values.min())
        self.vmax = kwargs.get('vmax', self.values.max())

    def recalculate_limits(self) -> None:
        self.vmin = self.values.min()
        self.vmax = self.values.max()

    """
    Data
    """
    @property
    def x(self) -> np.ndarray:
        return self.data[self._mapper.get('x')].to_numpy()

    @property
    def y(self) -> np.ndarray:
        return self.data[self._mapper.get('y')].to_numpy()

    @property
    def z(self) -> np.ndarray:
        return self.data[self._mapper.get('z')].to_numpy()

    @property
    def values(self) -> np.ndarray:
        return self.data[self._mapper.get('values')].to_numpy()

    @x.setter
    def x(self, _x: list) -> None:
        self.data[self._mapper.get('x')] = np.array(_x)

    @y.setter
    def y(self, _y: list) -> None:
        self.data[self._mapper.get('y')] = np.array(_y)

    @z.setter
    def z(self, _z: list) -> None:
        self.data[self._mapper.get('z')] = np.array(_z)

    @values.setter
    def values(self, _values) -> None:
        self.data[self._mapper.get('values')] = np.array(_values)

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
        return list(self._mapper.values())

    @property
    def is_slice(self) -> bool:
        return self.properties.get('is_slice', False)

    @colormap.setter
    def colormap(self, _colormap: str) -> None:
        if utils.parse_colormap(_colormap):  # Empty list interpreted as False
            self.properties['colormap'] = _colormap

    @vmin.setter
    def vmin(self, value: float) -> None:
        self.properties['vmin'] = float(value)

    @vmax.setter
    def vmax(self, value: float) -> None:
        self.properties['vmax'] = float(value)

    @headers.setter
    def headers(self, _headers: list) -> None:
        self._mapper['x'], self._mapper['y'], self._mapper['z'], self._mapper['values'] = _headers

    @is_slice.setter
    def is_slice(self, value: bool) -> None:
        self.properties['is_slice'] = value

    """
    Utilities
    """
    def slice_with_plane_and_threshold(self, origin: np.ndarray, normal: np.ndarray, threshold: float):
        """
        *** Plane Equation: ax + by + cz + d = 0 ***

        Where [a, b, c] = plane_normal
        Where [x, y, z] = plane_origin (or any point that we know belongs to the plane)

        With this, we can get `d`:
        dot([a, b, c], [x, y, z]) + d = 0
        d = -dot([a, b, c], [x, y, z])

        Since we have multiple vertices, it's easier to multiply plane_normal with
        each vertex, and manually sum them to get an array of dot products.

        But our points are blocks (they have 3D dimensions in `block_size`).
        That means we have to tolerate more points, so we will use a threshold.

        *** Plane Inequation: abs(ax + by + cz + d) <= threshold ***

        The projection idea comes from
        https://gdbooks.gitbooks.io/3dcollisions/content/Chapter2/static_aabb_plane.html
        """
        normal /= np.linalg.norm(normal)
        vertices = self.vertices

        plane_d = -np.dot(normal, origin)

        # In this context, np.inner(a, b) returns the same as (a * b).sum(axis=1), but it's faster.
        # Luckily, we don't run out of memory like in vectorized_triangles_intersection.
        mask = np.abs(np.inner(normal, vertices) + plane_d) <= threshold

        # If mask = [True, False, True], then mask.nonzero()[-1] = [0, 2]
        return mask.nonzero()[-1]
