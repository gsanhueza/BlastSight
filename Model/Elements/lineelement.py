#!/usr/bin/env python

import numpy as np
from random import random

from Model.Elements.element import Element


class LineElement(Element):
    def __init__(self, *args, **kwargs):
        self._values: np.ndarray = np.array([], np.float32)

        super().__init__(*args, **kwargs)
        assert len(self.vertices) >= 2
        self.values = [kwargs.get('color') for _ in range(len(self.vertices))]

    @property
    def values(self) -> np.ndarray:
        return self._values

    @values.setter
    def values(self, values: list):
        self._values = np.array(values, np.float32)
