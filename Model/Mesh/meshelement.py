#!/usr/bin/env python

import numpy as np
from random import random
from statistics import mean

from Model.element import Element


class MeshElement(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._indices = kwargs.get('indices')
        self._values = []

        assert len(self.x) >= self.indices.max() + 1

    @property
    def indices(self) -> np.array:
        return np.array(self._indices, np.uint32)  # GL_UNSIGNED_INT = np.uint32

    @indices.setter
    def indices(self, indices: list):
        self._indices = indices

    # FIXME Does this have to exist?
    @property
    def values(self) -> list:
        return list(map(lambda x: random(), range(3)))

    @values.setter
    def values(self, values: list):
        self._values = values
