#!/usr/bin/env python

import numpy as np
from random import random

from .element import Element


class LineElement(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if kwargs.get('loop', False):
            self.x = np.append(self.x, self.x[0])
            self.y = np.append(self.y, self.y[0])
            self.z = np.append(self.z, self.z[0])

        assert len(self.vertices) >= 2
        self.color = kwargs.get('color', [random() for _ in range(3)])

    @property
    def color(self) -> np.ndarray:
        return self._values

    @color.setter
    def color(self, color: list) -> None:
        self._values = np.array(color)
