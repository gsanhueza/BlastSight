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
        if kwargs.get('noautosize', False):
            self.block_size = kwargs.get('block_size', [1.0, 1.0, 1.0])
        else:
            self.block_size = kwargs.get('block_size', self._autosize(*args, **kwargs))

    def _autosize(self, *args, **kwargs):
        autosize = []

        for v in [self.x, self.y, self.z]:
            delta = np.abs(np.diff(v))
            autosize.append(float(min(delta[delta > 0.0], default=1.0)))

        return autosize

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
        self.properties['size'] = np.array(_size)
