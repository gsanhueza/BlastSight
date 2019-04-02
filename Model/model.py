#!/usr/bin/env python

from Model.Mesh.meshmanager import MeshManager
from Model.BlockModel.blockmodelhandler import BlockModelHandler


# Main class
class Model:
    def __init__(self):
        self.mesh_manager = MeshManager()
        self.blockmodel_handler = BlockModelHandler()

        self.vertices = None
        self.faces = None

    def get_vertices(self):
        return self.vertices

    def get_faces(self):
        return self.faces

    # The mesh handler will load the mesh and update our own data
    # Returns a boolean
    def load_mesh(self, filepath: str) -> bool:
        return self.mesh_manager.load_mesh(self, filepath)

    # The mesh handler will save the mesh by reading our own data
    # Returns a boolean
    def save_mesh(self, filepath: str) -> bool:
        return self.mesh_manager.save_mesh(self, filepath)

    # The block model handler will load the block model and update our own data
    # Returns a boolean
    def load_blockmodel(self, filepath: str) -> bool:
        return self.blockmodel_handler.load_mesh(self, filepath)

    # The block model handler will save the block model by reading our own data
    # Returns a boolean
    def save_blockmodel(self, filepath: str) -> bool:
        return self.blockmodel_handler.save_mesh(self, filepath)
