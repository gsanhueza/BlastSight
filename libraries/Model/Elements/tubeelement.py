#!/usr/bin/env python

import numpy as np
from random import random
from trimesh.creation import cylinder

from .element import Element


class TubeElement(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._radius = None
        self._resolution = None

        assert len(self.vertices) >= 2
        self.color = kwargs.get('color', [random() for _ in range(3)])
        self.radius = kwargs.get('radius', 0.15)
        self.resolution = kwargs.get('resolution', 15)

    @property
    def color(self) -> np.ndarray:
        return self._values

    @property
    def radius(self) -> float:
        return self._radius

    @property
    def resolution(self) -> int:
        return self._resolution

    @color.setter
    def color(self, color: list) -> None:
        self._values = np.array(color)

    @radius.setter
    def radius(self, value) -> None:
        self._radius = value

    @resolution.setter
    def resolution(self, value) -> None:
        self._resolution = value

    def as_mesh(self):
        vertices = []
        indices = []
        delta = 0

        for v1, v2 in zip(self.vertices[:-1], self.vertices[1:]):
            c = cylinder(radius=self.radius, sections=self.resolution, segment=[v1, v2])
            vertices.append(c.vertices)
            indices.append(c.faces + delta)
            delta += (c.faces.max() + 1)

        return np.concatenate(vertices), np.concatenate(indices)
