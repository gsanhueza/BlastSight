#!/usr/bin/env python

import numpy as np
from .dfelement import DFElement
from ..utils import hsv_to_rgb


class PointElement(DFElement):
    def __init__(self, *args, **kwargs):
        """
        PointElement is a class inheriting from DFElement.

        {
            'data': {
                'x': list[float],
                'y': list[float],
                'z': list[float],
                'values: list[float],
            },
            'properties': {
                'header_position': list[str],
                'header_value': str,
                'vmin': float,
                'vmax': float,
                'size': list[float],
                'alpha': float,
                'colormap': str
            }
            'metadata': {
                'id': int,
                'name': str or None,
                'extension': str or None
            }
        }

        Where 'data' will be implemented as a Pandas DataFrame.
        """
        super().__init__(*args, **kwargs)

    def _fill_properties(self, *args, **kwargs):
        super()._fill_properties(*args, **kwargs)
        self.marker = kwargs.get('marker', 'circle')
        self.colormap = kwargs.get('colormap', 'redblue')  # redblue (min is red) or bluered (min is blue)
        self.colors = kwargs.get('color', self.values_to_rgb(self.values, self.vmin, self.vmax, self.colormap))

    def _fill_size(self, *args, **kwargs):
        self.point_size = kwargs.get('point_size', [1.0] * self.x.size)

    """
    Properties
    """
    @property
    def point_size(self) -> np.ndarray:
        return self.properties.get('size')

    @property
    def marker(self) -> str:
        return self.properties.get('marker')

    @property
    def colors(self):
        return self.properties.get('colors')

    @property
    def colormap(self) -> str:
        return self.properties.get('colormap')

    @point_size.setter
    def point_size(self, size) -> None:
        self.properties['size'] = np.tile(size, self.x.size) if type(size) is float else np.array(size)

    @marker.setter
    def marker(self, _marker: str) -> None:
        self.properties['marker'] = _marker

    @colors.setter
    def colors(self, _colors: list):
        self.properties['colors'] = np.array(_colors)

    @colormap.setter
    def colormap(self, _colormap: str) -> None:
        self.properties['colormap'] = _colormap

    """
    Utilities
    """
    @staticmethod
    def values_to_rgb(values, vmin, vmax, colormap):
        values = np.clip(values, vmin, vmax)
        norm = values.max() - values.min()
        if norm == 0:
            return np.ones(3 * values.size)

        vals = (values - values.min()) / norm
        hsv = np.ones((vals.size, 3))

        if colormap == 'redblue':
            hsv[:, 0] = 2 / 3 * vals
        elif colormap == 'bluered':
            hsv[:, 0] = 2 / 3 * (1.0 - vals)

        return hsv_to_rgb(hsv)
