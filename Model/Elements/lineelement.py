#!/usr/bin/env python

import numpy as np

from Model.Elements.element import Element


class LineElement(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert len(self.vertices) >= 2
        assert 'color' in kwargs.keys()
        self.color = kwargs.get('color')

    @property
    def color(self) -> np.ndarray:
        return self._values

    @color.setter
    def color(self, values: list):
        self._values = np.array(values, np.float32)
