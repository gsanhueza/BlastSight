#!/usr/bin/env python

from Model.handler import Handler
from Model.BlockModel.csvparser import CSVParser


# OFF handler for mesh loading/saving
class CSVHandler(Handler):
    def __init__(self):
        self.parser = CSVParser()

    # Loads a CSV file and updates the model
    def load_mesh(self, model, filepath):
        try:
            self.parser.load_file(filepath)
            model.vertices = self.parser.get_vertices()
            model.faces = self.parser.get_faces()
            return True
        except Exception:
            return False

    # Saves an CSV file
    def save_mesh(self, filepath=None):
        # TODO Create a new file on filepath
        # TODO Write the CSV
        # TODO Close the file
        return False
