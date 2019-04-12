#!/usr/bin/env python

from View.drawable import Drawable


# Composite Pattern
class GLDrawableCollection(Drawable):
    def __init__(self):
        super().__init__()
        self.drawable_list = []

    def add(self, drawable):
        self.drawable_list.append(drawable)

    def draw(self):
        for drawable in self.drawable_list:
            drawable.draw()
