#!/usr/bin/env python

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

    def _fill_element(self, *args, **kwargs):
        super()._fill_element(*args, **kwargs)
        if len(self.vertices) < 2:
            raise ValueError("Not enough data to create this element.")

        if kwargs.get('loop', False):
            self.x = np.append(self.x, self.x[0])
            self.y = np.append(self.y, self.y[0])
            self.z = np.append(self.z, self.z[0])
