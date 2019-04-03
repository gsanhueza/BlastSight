#!/usr/bin/env python

from Model.Mesh.dxfparser import DXFParser
from Model.handler import Handler


# DXF handler for mesh loading/saving
class DXFHandler(Handler):
    def __init__(self):
        self.parser = DXFParser()

    # Loads a DXF file and updates the model
    def load_mesh(self, model, file_path):
        try:
            self.parser.load_file(file_path)
            # FIXME Not average vertices!
            model.vertices = self.parser.get_averaged_vertices()
            model.indices = self.parser.get_indices()
            return True
        except Exception:
            return False

    # Saves a DXF file and updates the model
    def save_mesh(self, model, file_path):
        raise NotImplementedError
