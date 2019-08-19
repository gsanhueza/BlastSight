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
                'size': list[list[float]],
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

        Where 'data' will be implemented as a Pandas DataFrame.
        """
        super().__init__(*args, **kwargs)

    def _fill_properties(self, *args, **kwargs):
        super()._fill_properties(*args, **kwargs)
        self.marker = kwargs.get('marker', 'circle')
        self.colormap = kwargs.get('colormap', 'redblue')  # redblue (min is red) or bluered (min is blue)
        self.color = kwargs.get('color', [])

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
    def color(self):
        if self.properties.get('color').size == 0:
            return self.values_to_rgb(self.values, self.vmin, self.vmax, self.colormap)
        return self.properties.get('color')

    @property
    def colormap(self) -> str:
        return self.properties.get('colormap')

    @point_size.setter
    def point_size(self, size) -> None:
        self.properties['size'] = np.tile(size, self.x.size) if type(size) is float else np.array(size)

    @marker.setter
    def marker(self, _marker: str) -> None:
        self.properties['marker'] = _marker

    @color.setter
    def color(self, _colors: list):
        self.properties['color'] = np.array(_colors)

    @colormap.setter
    def colormap(self, _colormap: str) -> None:
        self.properties['colormap'] = _colormap

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

        hsv[:, 0] = PointElement.color_from_dict(colormap)(vals)
        return hsv_to_rgb(hsv)
