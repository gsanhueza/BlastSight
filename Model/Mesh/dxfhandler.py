#!/usr/bin/env python

from Model.Mesh.dxfparser import DXFParser
from Model.handler import Handler


# DXF handler for mesh loading/saving
class DXFHandler(Handler):
    def __init__(self):
        self.parser = DXFParser()

    def load_mesh(self, model, file_path):
        # FIXME Not average vertices!
        self.parser.load_file(file_path)
        model.vertices = self.parser.get_averaged_vertices()
        model.indices = self.parser.get_indices()
        model.values = self.parser.get_values()

        return True

    # Saves a DXF file and updates the model
    def save_mesh(self, model, file_path):
        raise NotImplementedError
