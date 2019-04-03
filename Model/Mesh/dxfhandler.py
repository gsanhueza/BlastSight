#!/usr/bin/env python

from Model.Mesh.dxfparser import DXFParser
from Model.handler import Handler


# DXF handler for mesh loading/saving
class DXFHandler(Handler):
    def __init__(self):
        self.parser = DXFParser()

    # Loads a DXF file and updates the model
    def load_mesh(self, model, filepath):
        try:
            self.parser.load_file(filepath)
            model.vertices = self.parser.get_averaged_vertices()  # FIXME Not average vertices!
            model.faces = self.parser.get_faces()
            return True
        except Exception:
            return False

    # Saves a DXF file and updates the model
    def save_mesh(self, filepath=None):
        # TODO Create a new file on filepath
        # TODO Write the DXF with the model's vertices and faces (dxfgrabber?)
        # TODO Close the file
        return False
