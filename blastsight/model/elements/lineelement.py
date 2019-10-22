#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np
from .element import Element


class LineElement(Element):
    def __init__(self, *args, **kwargs):
        """
        LineElement is a class inheriting from Element.

        {
            'data': {
                'x': list[float],
                'y': list[float],
                'z': list[float],
            }
            'properties': {
                'color': list[float],
                'alpha': float
            },
            'metadata': {
                'id': int,
                'name': str or None,
                'extension': str or None
            }
        }
        """
        super().__init__(*args, **kwargs)

    def _fill_properties(self, *args, **kwargs):
        super()._fill_properties(*args, **kwargs)
        self.loop = kwargs.get('loop', False)

    def _check_integrity(self):
        super()._check_integrity()
        if len(self.vertices) < 2:
            raise ValueError("Not enough data to create this element.")

        # Append first vertex to self.vertices if a loop was enabled
        if self.loop:
            self.vertices = np.append(self.vertices, [self.vertices[0, :]], axis=0)

    @property
    def loop(self):
        return self.properties.get('loop')

    @loop.setter
    def loop(self, _loop: bool):
        self.properties['loop'] = _loop
