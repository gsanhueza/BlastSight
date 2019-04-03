#!/usr/bin/env python

from Model.handler import Handler
from Model.Mesh.offparser import OFFParser


# OFF handler for mesh loading/saving
class OFFHandler(Handler):
    def __init__(self):
        self.parser = OFFParser()

    # Loads a OFF file and updates the model
    def load_mesh(self, model, file_path):
        try:
            self.parser.load_file(file_path)
            model.vertices = self.parser.get_vertices()
            model.faces = self.parser.get_indices()
            return True
        except Exception:
            return False

    # Saves an OFF file and updates the model
    def save_mesh(self, model, file_path):
        raise NotImplementedError
