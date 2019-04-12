#!/usr/bin/env python

from Model.Mesh.meshelement import MeshElement
from Model.BlockModel.blockmodelelement import BlockModelElement


# Main class
class Model:
    def __init__(self):
        self.mesh = MeshElement()
        self.block_model = BlockModelElement()

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
        return self.mesh.load(file_path)

    def save_mesh(self, file_path: str) -> bool:
        return self.mesh.save(file_path)

    def load_block_model(self, file_path: str) -> bool:
        return self.block_model.load(file_path)

    def save_block_model(self, file_path: str) -> bool:
        return self.block_model.save(file_path)
