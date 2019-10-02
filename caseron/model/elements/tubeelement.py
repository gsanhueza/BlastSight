#!/usr/bin/env python

import numpy as np
from .element import Element
from . import tubeutils


class TubeElement(Element):
    def __init__(self, *args, **kwargs):
        """
        TubeElement is a class inheriting from Element.

        {
            'data': {
                'x': list[float],
                'y': list[float],
                'z': list[float],
            }
            'properties': {
                'color': list[float],
                'alpha': float,
                'radius': float,
                'resolution': int
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

    def _fill_properties(self, *args, **kwargs):
        super()._fill_properties(*args, **kwargs)
        self.radius = kwargs.get('radius', 0.15)
        self.resolution = kwargs.get('resolution', 15)

    """
    Properties
    """
    @property
    def radius(self) -> float:
        return self.properties.get('radius')

    @property
    def resolution(self) -> int:
        return self.properties.get('resolution')

    @radius.setter
    def radius(self, _radius: float) -> None:
        self.properties['radius'] = _radius

    @resolution.setter
    def resolution(self, _resolution: int) -> None:
        self.properties['resolution'] = _resolution

    """
    Utilities
    """
    def as_mesh(self):
        vertices = []
        indices = []
        delta = 0

        for v0, v1 in zip(self.vertices[:-1], self.vertices[1:]):
            c_vertices, c_faces = tubeutils.cylinder(self.radius, self.resolution, [v0, v1])
            vertices.append(c_vertices)
            indices.append(c_faces + delta)
            delta += (c_faces.max() + 1)

        return np.concatenate(vertices), np.concatenate(indices)
