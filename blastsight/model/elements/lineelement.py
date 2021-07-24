#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np

from .element import Element
from ..intersections import Intersections
from .. import utils


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
                'thickness': int,
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

    def _fill_properties(self, *args, **kwargs) -> None:
        super()._fill_properties(*args, **kwargs)
        self.thickness = kwargs.get('thickness', 1.0)
        self.loop = kwargs.get('loop', False)

    def _check_integrity(self) -> None:
        super()._check_integrity()
        if len(self.vertices) < 2:
            raise ValueError("Not enough data to create this element.")

        # Append first vertex to self.vertices if a loop was enabled
        if self.loop:
            self.vertices = np.append(self.vertices, [self.vertices[0, :]], axis=0)

    @property
    def loop(self) -> bool:
        return self.properties.get('loop')

    @property
    def thickness(self) -> int:
        return self.properties.get('thickness')

    @loop.setter
    def loop(self, _loop: bool) -> None:
        self.properties['loop'] = _loop

    @thickness.setter
    def thickness(self, value: float) -> None:
        self.properties['thickness'] = value

    """
    Utilities
    """
    def intersect_with_ray(self, origin: np.ndarray, ray: np.ndarray) -> np.ndarray:
        # Early AABB detection test
        if not Intersections.aabb_intersection(origin, ray, *self.bounding_box):
            return np.empty(0)

        return Intersections.ray_with_lines(origin, ray, self.vertices)
