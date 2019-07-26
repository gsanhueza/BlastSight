#!/usr/bin/env python

import numpy as np
from random import random

from .element import Element


class MeshElement(Element):
    def __init__(self, *args, **kwargs):
        self._indices: np.ndarray = np.array([], np.float32)

        super().__init__(*args, **kwargs)

        self.indices = kwargs.get('indices', [])
        self.values = kwargs.get('color', list(map(lambda x: random(), range(3))))

        assert self.x.size == self.indices.max() + 1

    @property
    def indices(self) -> np.array:
        return self._indices

    @indices.setter
    def indices(self, indices):
        self._indices = np.array(indices, np.uint32)  # GL_UNSIGNED_INT = np.uint32
