#!/usr/bin/env python

import numpy as np
from random import random

from Model.Elements.element import Element


class LineElement(Element):
    def __init__(self, *args, **kwargs):
        self._color: np.ndarray = np.array([], np.float32)

        super().__init__(*args, **kwargs)
        assert len(self.vertices) >= 2
        self.color = kwargs.get('color')

    @property
    def color(self) -> np.ndarray:
        return self._values

    @color.setter
    def color(self, values: list):
        self._values = np.array(values, np.float32)