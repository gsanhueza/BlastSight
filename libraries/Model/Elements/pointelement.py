#!/usr/bin/env python

import numpy as np
from .dfelement import DFElement


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
