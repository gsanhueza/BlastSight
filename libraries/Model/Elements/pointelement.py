#!/usr/bin/env python

from .blockmodelelement import BlockModelElement


class PointElement(BlockModelElement):
    """
    Points and block models are interpreted as almost the same. (Model)
    The difference is at drawing time. (View)
    """
    def _fill_size(self, *args, **kwargs):
        self.point_size = kwargs.get('point_size', 1.0)

    @property
    def point_size(self):
        return self._size

    @point_size.setter
    def point_size(self, size) -> None:
        self._size = size

    @property
    def marker(self):
        return self._properties.get('marker', 'circle')
