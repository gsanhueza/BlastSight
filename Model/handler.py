#!/usr/bin/env python

from PySide2.QtCore import QFileInfo


class Handler:
    def __init__(self):
        self.parser = None

    # Loads a DXF file and updates the model
    def load_mesh(self, model, file_path: str) -> bool:
        self.parser.load_file(file_path)
        model.mesh_vertices = self.parser.get_vertices()
        model.mesh_indices = self.parser.get_indices()
        model.mesh_values = self.parser.get_values()
        return True

    def save_mesh(self, model, file_path):
        # TODO Save mesh
        return False

    @staticmethod
    def get_file_extension(file_path: str) -> str:
        file_info = QFileInfo(file_path)
        return file_info.suffix()
