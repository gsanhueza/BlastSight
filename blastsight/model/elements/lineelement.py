#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np
from .element import Element
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
        if not utils.aabb_intersection(origin, ray, *self.bounding_box):
            return np.empty(0)

        return self.vectorized_intersection(origin, ray)

    # Adapted from https://www.codefull.net/2015/06/intersection-of-a-ray-and-a-line-segment-in-3d/
    def vectorized_intersection(self, origin: np.ndarray, ray: np.ndarray, threshold: float = 1e-2) -> np.ndarray:
        ba = np.diff(self.vertices, axis=0)
        ao = self.vertices[:-1] - origin

        ao_x_ba = np.cross(ao, ba)
        ray_x_ba = np.cross(ray, ba)

        # How much does the ray need to travel to arrive to the (infinite) line, for each segment
        s = utils.dot_by_row(ao_x_ba, ray_x_ba) / utils.magnitude2_by_row(ray_x_ba)

        # All intersections with infinite lines
        intersections = origin + s.reshape(-1, 1) * ray

        length_ai = utils.magnitude_by_row(intersections - self.vertices[:-1])
        length_ib = utils.magnitude_by_row(intersections - self.vertices[1:])
        length_ab = utils.magnitude_by_row(ba)

        # Mask is True if the ray and line are coplanar enough
        mask_threshold = abs(utils.dot_by_row(ao, ray_x_ba)) < threshold

        # Mask is True if the ray is between the start and end of each segment
        mask_inside = length_ai + length_ib <= length_ab + threshold

        return intersections[mask_threshold & mask_inside]
