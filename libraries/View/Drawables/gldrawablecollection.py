#!/usr/bin/env python

from collections import OrderedDict
from .gldrawable import GLDrawable


class GLDrawableCollection(OrderedDict):
    def add(self, id_: int, drawable: GLDrawable) -> None:
        self.__setitem__(id_, drawable)

    def draw(self, proj_matrix, view_matrix, model_matrix) -> None:
        for drawable in self.values():
            if not drawable.is_initialized:
                drawable.initialize()

            drawable.draw(proj_matrix, view_matrix, model_matrix)
