#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

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
            'datasets': {
                'color': list[list[float]] (Optional, auto-generated from 'values' if None)
            },
            'properties': {
                'headers': list[str],
                'vmin': float,
                'vmax': float,
                'alpha': float,
                'size': float,
                'colormap': str (Optional, used from 'values')
            }
            'metadata': {
                'id': int,
                'name': str or None,
                'extension': str or None
            }
        }

        In a BlockElement, all blocks have the same 3D size, but each block has its own color.
        If the user didn't specify colors, they will be auto-calculated from 'values' and 'colormap'.
        The rest of the explanation is in DFElement class.
        """
        super().__init__(*args, **kwargs)

    def _fill_properties(self, *args, **kwargs):
        super()._fill_properties(*args, **kwargs)
        if kwargs.get('autosize', True):
            self.block_size = kwargs.get('block_size', self.get_autosize())
        else:
            self.block_size = kwargs.get('block_size', [1.0, 1.0, 1.0])

    def get_autosize(self) -> np.ndarray:
        size = []

        for v in [self.x, self.y, self.z]:
            delta = np.abs(np.diff(v))
            size.append(float(min(delta[delta > 0.0], default=1.0)))

        return np.array(size)

    """
    Properties
    """
    @property
    def customizable_properties(self):
        return ['alpha', 'colormap', 'vmin', 'vmax', 'block_size']

    @property
    def exportable_properties(self):
        return ['alpha', 'colormap', 'headers', 'block_size']

    @property
    def block_size(self) -> np.ndarray:
        return self.properties.get('size')

    @block_size.setter
    def block_size(self, _size: list) -> None:
        self.properties['size'] = np.array(_size) if len(_size) == 3 else np.array(self.get_autosize())

    @property
    def bounding_box(self) -> tuple:
        lo, hi = super().bounding_box
        return lo - (self.block_size / 2), hi + (self.block_size / 2)
