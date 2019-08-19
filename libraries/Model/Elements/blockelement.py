#!/usr/bin/env python

import numpy as np
from .dfelement import DFElement


class BlockElement(DFElement):
    def __init__(self, *args, **kwargs):
        """
        BlockElement is a class inheriting from PointElement (which inherits from DFElement).

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
        self.colormap = kwargs.get('colormap', 'redblue')  # redblue (min is red) or bluered (min is blue)
        self.color = kwargs.get('color', [])

    def _fill_size(self, *args, **kwargs):
        self.block_size = kwargs.get('block_size', [1.0, 1.0, 1.0])
    """
    Properties
    """
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
    def block_size(self) -> np.ndarray:
        return self.properties.get('size')

    @block_size.setter
    def block_size(self, _size: list) -> None:
        self.properties['size'] = np.array(_size)
