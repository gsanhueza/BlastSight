#!/usr/bin/env python

import numpy as np
from random import random

from Model.Elements.element import Element


class MeshElement(Element):
    def __init__(self, *args, **kwargs):
        self._indices: np.ndarray = np.array([], np.float32)
        self._values: np.ndarray = np.array([], np.float32)

        super().__init__(*args, **kwargs)

        self.indices = kwargs.get('indices')
        self.values = list(map(lambda x: random(), range(3)))
        assert self.x.size >= self.indices.max() + 1

    @property
    def indices(self) -> np.array:
        return self._indices

    @indices.setter
    def indices(self, indices: list):
        self._indices = np.array(indices, np.uint32)  # GL_UNSIGNED_INT = np.uint32

    @property
    def values(self) -> np.ndarray:
        return self._values

    @values.setter
    def values(self, values: list):
        self._values = np.array(values, np.float32)
