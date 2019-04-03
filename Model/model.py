#!/usr/bin/env python

from Model.Mesh.meshmanager import MeshManager
from Model.BlockModel.blockmodelmanager import BlockModelManager


# Main class
class Model:
    def __init__(self):
        self.mesh_manager = MeshManager()
        self.block_model_manager = BlockModelManager()

        self.vertices = None
        self.indices = None

    def get_vertices(self):
        return self.vertices

    def get_indices(self):
        return self.indices

    # The mesh handler will load the mesh and update our own data
    # Returns a boolean
    def load_mesh(self, file_path: str) -> bool:
        return self.mesh_manager.load_mesh(self, file_path)

    # The mesh handler will save the mesh by reading our own data
    # Returns a boolean
    def save_mesh(self, file_path: str) -> bool:
        return self.mesh_manager.save_mesh(self, file_path)

    # The block model handler will load the block model and update our own data
    # Returns a boolean
    def load_block_model(self, file_path: str) -> bool:
        return self.block_model_manager.load_block_model(self, file_path)

    # The block model handler will save the block model by reading our own data
    # Returns a boolean
    def save_block_model(self, file_path: str) -> bool:
        return self.block_model_manager.save_block_model(self, file_path)
