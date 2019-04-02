#/usr/bin/env python

from .offparser import OFFParser


# DXF handler for mesh loading/saving
class OFFHandler:
    def __init__(self):
        self.parser = OFFParser()

    # Loads a DXF file and updates the model
    def load_mesh(self, model, filepath):
        try:
            self.parser.load_file(filepath)
            model.vertices = self.parser.get_vertices()
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
