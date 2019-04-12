#!/usr/bin/env python

from Model.filemanager import FileManager
from Model.modelelement import ModelElement


# Main class
class Model:
    def __init__(self):
        self.file_manager = FileManager()
        self.mesh = ModelElement()
        self.block_model = ModelElement()

    def get_mesh_vertices(self):
        return self.mesh.get_vertices()

    def get_mesh_indices(self):
        return self.mesh.get_indices()

    def get_mesh_values(self):
        return self.mesh.get_values()

    def get_block_model_vertices(self):
        return self.block_model.get_vertices()

    def get_block_model_indices(self):
        return self.block_model.get_indices()

    def get_block_model_values(self):
        return self.block_model.get_values()

    def load_mesh(self, file_path: str) -> bool:
        return self.file_manager.load_mesh(self.mesh, file_path)

    def save_mesh(self, file_path: str) -> bool:
        return self.file_manager.save_mesh(self.mesh, file_path)

    def load_block_model(self, file_path: str) -> bool:
        return self.file_manager.load_block_model(self.block_model, file_path)

    def save_block_model(self, file_path: str) -> bool:
        return self.file_manager.save_block_model(self.block_model, file_path)
