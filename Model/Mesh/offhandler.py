#!/usr/bin/env python

from Model.handler import Handler
from Model.Mesh.offparser import OFFParser


# OFF handler for mesh loading/saving
class OFFHandler(Handler):
    def __init__(self):
        self.parser = OFFParser()

    # Loads a OFF file and updates the model
    def load_mesh(self, model, filepath):
        try:
            self.parser.load_file(filepath)
            model.vertices = self.parser.get_vertices()
            model.faces = self.parser.get_faces()
            return True
        except Exception:
            return False

    # Saves an OFF file and updates the model
    def save_mesh(self, filepath=None):
        # TODO Create a new file on filepath
        # TODO Write the OFF with the model's vertices and faces
        # TODO Close the file
        return False
