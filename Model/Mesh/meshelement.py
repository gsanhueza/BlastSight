#!/usr/bin/env python

import numpy as np
from statistics import mean

from Model.element import Element


class MeshElement(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.indices = np.array(kwargs.get('indices'), np.uint32)
        self.centroid = list(map(mean, [self.x, self.y, self.z]))

        assert len(self.x) >= self.indices.max() + 1

    def get_indices(self) -> np.array:
        return np.array(self.indices, np.uint32)  # GL_UNSIGNED_INT = np.uint32

    def get_centroid(self):
        return self.centroid

    # FIXME Does this have to exist?
    def get_values(self):
        from random import random
        return list(map(lambda x: random(), range(3)))
