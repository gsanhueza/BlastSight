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
            'datasets': {
                'size': list[float], (Each point has its own size in 1D)
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

        In a PointElement, each point has its own 1D size, and each block has its own color.
        If the user didn't specify colors, they will be auto-calculated from 'values' and 'colormap'.
        The rest of the explanation is in DFElement class.
        """
        super().__init__(*args, **kwargs)
        self.marker_dict = {
            'square': 0,
            'circle': 1,
            'sphere': 2,
        }

    def _fill_properties(self, *args, **kwargs):
        super()._fill_properties(*args, **kwargs)
        self.marker = kwargs.get('marker', 'square')
        self.point_size = kwargs.get('point_size', float(kwargs.get('avg_size', 1.0)))

    """
    Properties
    """
    @property
    def customizable_properties(self):
        return ['alpha', 'colormap', 'vmin', 'vmax', 'marker', 'avg_size']

    @property
    def exportable_properties(self):
        return ['alpha', 'colormap', 'headers', 'marker', 'avg_size']

    @property
    def avg_size(self) -> float:
        return self.point_size.mean()

    @property
    def point_size(self) -> np.ndarray:
        return self.datasets.get('size')

    @property
    def marker_num(self) -> int:
        return self.marker_dict.get(self.marker, 0)

    @property
    def marker(self) -> str:
        return self.properties.get('marker', 'square')

    @avg_size.setter
    def avg_size(self, _avg_size: float):
        self.point_size = _avg_size

    @point_size.setter
    def point_size(self, _size) -> None:
        if type(_size) is float:
            self.datasets['size'] = np.tile(_size, self.x.size).astype(np.float32)
        else:
            self.datasets['size'] = np.array(_size, np.float32)

    @marker.setter
    def marker(self, _marker: str) -> None:
        self.properties['marker'] = _marker