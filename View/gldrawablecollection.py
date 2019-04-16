#!/usr/bin/env python

from collections import OrderedDict


class GLDrawableCollection:
    def __init__(self):
        super().__init__()
        self.drawable_dict = OrderedDict()

    def __getitem__(self, item):
        return self.drawable_dict[item]

    def __setitem__(self, key, value):
        self.drawable_dict[key] = value

    def add(self, id_, drawable):
        self.drawable_dict[id_] = drawable

    def draw(self):
        for drawable in self.drawable_dict.values():
            if not drawable.is_initialized:
                drawable.initialize()

            drawable.draw()

    def clear(self):
        self.drawable_dict.clear()
