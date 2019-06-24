#!/usr/bin/env python

import numpy as np
from .pointelement import PointElement


class BlockModelElement(PointElement):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def block_size(self) -> np.ndarray:
        return self.point_size

    @block_size.setter
    def block_size(self, size: list) -> None:
        self.point_size = np.array(size, np.float32)
