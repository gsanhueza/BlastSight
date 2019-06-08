#!/usr/bin/env python

import numpy as np

from .element import Element


class TubeElement(Element):
    def __init__(self, *args, **kwargs):
        self._radius = None
        self._resolution = None

        super().__init__(*args, **kwargs)

        assert len(self.vertices) >= 2
        assert 'radius' in kwargs.keys()
        assert 'resolution' in kwargs.keys()
        assert 'color' in kwargs.keys()

        self.color = kwargs.get('color')
        self.radius = kwargs.get('radius')
        self.resolution = kwargs.get('resolution')

    @property
    def color(self) -> np.ndarray:
        return self._values

    @color.setter
    def color(self, color: list) -> None:
        self._values = np.array(color, np.float32)

    @property
    def radius(self) -> int:
        return self._radius

    @radius.setter
    def radius(self, radius: int) -> None:
        self._radius = radius

    @property
    def resolution(self) -> int:
        return self._resolution

    @resolution.setter
    def resolution(self, resolution: int) -> None:
        self._resolution = resolution
