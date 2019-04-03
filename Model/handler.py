#!/usr/bin/env python

from abc import abstractmethod


class Handler:
    def __init__(self):
        pass

    @abstractmethod
    def load_mesh(self, model, filepath):
        return False

    @abstractmethod
    def save_mesh(self, filepath):
        # TODO Create a new file on filepath
        # TODO Write the DXF with the model's vertices and faces (dxfgrabber?)
        # TODO Close the file
        return False
