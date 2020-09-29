#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
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

    def _fill_properties(self, *args, **kwargs) -> None:
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

    def recalculate_limits(self) -> None:
        super().recalculate_limits()
        self.block_size = self.get_autosize()

    """
    Properties
    """
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

    """
    Utilities
    """
    def slice_with_plane(self, origin: np.ndarray, normal: np.ndarray) -> np.ndarray:
        """
        *** Plane Equation: ax + by + cz + d = 0 ***

        Where [a, b, c] = plane_normal
        Where [x, y, z] = plane_origin (or any point that we know belongs to the plane)

        With this, we can get `d`:
        dot([a, b, c], [x, y, z]) + d = 0
        d = -dot([a, b, c], [x, y, z])

        Since we have multiple vertices, it's easier to multiply plane_normal with
        each vertex, and manually sum them to get an array of dot products.

        But our points are blocks (they have 3D dimensions in `block_size`).
        That means we have to tolerate more points, so we create a threshold.

        *** Plane Inequation: abs(ax + by + cz + d) <= threshold ***

        We need to know how inclined is the plane normal to know our threshold.
        Let's say our block_size is [10, 10, 10] (half_block is [5, 5, 5]).

        If the plane touches one face of the cube, our threshold is [-5, +5] * np.sqrt(1.0).
        If the plane touches one edge of the cube, our threshold is [-5, +5] * np.sqrt(2.0).
        If the plane touches one vertex of the cube, our threshold is [-5, +5] * np.sqrt(3.0).

        Since a cube is symmetrical by axes, we don't really care about the plane normal's signs.
        Then, we'll calculate np.dot(abs(plane_normal), half_block) to know the maximum
        tolerable distance between the cube center and its projection on the plane.

        The projection idea comes from
        https://gdbooks.gitbooks.io/3dcollisions/content/Chapter2/static_aabb_plane.html
        """
        normal /= np.linalg.norm(normal)
        half_block = np.array(self.block_size) / 2
        vertices = self.vertices

        plane_d = -np.dot(normal, origin)
        threshold = np.dot(np.abs(normal), half_block)

        # In this context, np.inner(a, b) returns the same as (a * b).sum(axis=1), but it's faster.
        # Luckily, we don't run out of memory like in vectorized_triangles_intersection.
        mask = np.abs(np.inner(normal, vertices) + plane_d) <= threshold

        # If mask = [True, False, True], then mask.nonzero()[-1] = [0, 2]
        return mask.nonzero()[-1]
