#!/usr/bin/env python

import numpy as np
from random import random

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
        self._values = np.array(color, np.float32)

    @radius.setter
    def radius(self, value) -> None:
        self._radius = value

    @resolution.setter
    def resolution(self, value) -> None:
        self._resolution = value
