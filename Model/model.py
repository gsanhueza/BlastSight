#!/usr/bin/env python

from Model.filemanager import FileManager


# Main class
class Model:
    def __init__(self):
        self.file_manager = FileManager()

        self.mesh_vertices = None
        self.mesh_indices = None
        self.mesh_values = None

        self.block_model_vertices = None
        self.block_model_indices = None
        self.block_model_values = None

    def get_mesh_vertices(self):
        return self.mesh_vertices

    def get_mesh_indices(self):
        return self.mesh_indices

    def get_mesh_values(self):
        return self.mesh_values

    def get_block_model_vertices(self):
        return self.block_model_vertices

    def get_block_model_indices(self):
        return self.block_model_indices

    def get_block_model_values(self):
        return self.block_model_values

    def load_mesh(self, file_path: str) -> bool:
        return self.file_manager.load_mesh(self, file_path)

    def save_mesh(self, file_path: str) -> bool:
        return self.file_manager.save_mesh(self, file_path)

    def load_block_model(self, file_path: str) -> bool:
        return self.file_manager.load_block_model(self, file_path)

    def save_block_model(self, file_path: str) -> bool:
        return self.file_manager.save_block_model(self, file_path)
