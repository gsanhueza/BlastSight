#!/usr/bin/env python


# Main class
class ModelElement:
    def __init__(self):
        self.vertices = None
        self.indices = None
        self.values = None

    def get_vertices(self):
        return self.vertices

    def get_indices(self):
        return self.indices

    def get_values(self):
        return self.values

    def set_vertices(self, vertices):
        self.vertices = vertices

    def set_indices(self, indices):
        self.indices = indices

    def set_values(self, values):
        self.values = values
