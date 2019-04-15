#!/usr/bin/env python

from View.drawable import Drawable


# Composite Pattern
class GLDrawableCollection(Drawable):
    def __init__(self):
        super().__init__()
        self.drawable_list = []

    def __getitem__(self, item):
        return self.drawable_list[item]

    def add(self, drawable):
        self.drawable_list.append(drawable)

    def draw(self):
        for drawable in self.drawable_list:
            if not drawable.is_initialized:
                drawable.initialize()

            drawable.draw()

    def clear(self):
        self.drawable_list.clear()
