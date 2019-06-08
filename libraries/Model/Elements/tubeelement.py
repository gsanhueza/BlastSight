#!/usr/bin/env python

import numpy as np

from .element import Element


class TubeElement(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        assert len(self.vertices) >= 2
        assert 'color' in kwargs.keys()

        self.color = kwargs.get('color')

    @property
    def color(self) -> np.ndarray:
        return self._values

    @color.setter
    def color(self, color: list) -> None:
        self._values = np.array(color, np.float32)
