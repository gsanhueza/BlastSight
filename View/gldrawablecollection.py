#!/usr/bin/env python

from collections import OrderedDict
from View.gldrawable import GLDrawable


class GLDrawableCollection:
    def __init__(self):
        super().__init__()
        self.drawable_dict = OrderedDict()

    def __getitem__(self, key: int):
        return self.drawable_dict[key]

    def __setitem__(self, key: int, value: GLDrawable) -> None:
        self.drawable_dict[key] = value

    def __len__(self) -> int:
        return self.drawable_dict.__len__()

    def __delitem__(self, key):
        self.drawable_dict.__delitem__(key)

    def items(self):
        return self.drawable_dict.items()

    """
    Custom methods
    """

    def add(self, id_: int, drawable: GLDrawable) -> None:
        self.drawable_dict[id_] = drawable

    def draw(self) -> None:
        for drawable in self.drawable_dict.values():
            if not drawable.is_initialized:
                drawable.initialize()

            drawable.draw()

    def clear(self) -> None:
        self.drawable_dict.clear()
