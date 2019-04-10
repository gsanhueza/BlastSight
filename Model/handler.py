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

    def save_mesh(self, model, file_path: str) -> bool:
        # TODO Save mesh
        return False

    def load_block_model(self, model, file_path: str) -> bool:
        self.parser.load_file(file_path)
        model.block_model_vertices = self.parser.get_vertices()
        model.block_model_indices = self.parser.get_indices()
        model.block_model_values = self.parser.get_values()
        return True

    def save_block_model(self, model, file_path: str) -> bool:
        # TODO Save block model
        return False

    @staticmethod
    def get_file_extension(file_path: str) -> str:
        file_info = QFileInfo(file_path)
        return file_info.suffix()
