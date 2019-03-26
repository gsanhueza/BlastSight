#!/usr/bin/env python

from .Mesh.meshhandler import MeshHandler
from .BlockModel.blockmodelhandler import BlockModelHandler


# Main class
class Model:
    def __init__(self):
        self.mesh_handler = MeshHandler()
        self.blockmodel_handler = BlockModelHandler()

        self.vertices = None
        self.faces = None

    # The mesh handler will load the mesh and update our own data
    # Returns a boolean
    def load_mesh(self, filepath):
        return self.mesh_handler.load_mesh(self, filepath)

    # The mesh handler will save the mesh by reading our own data
    # Returns a boolean
    def save_mesh(self, filepath):
        return self.mesh_handler.save_mesh(self, filepath)

    # The block model handler will load the block model and update our own data
    # Returns a boolean
    def load_blockmodel(self, filepath):
        return self.blockmodel_handler.load_mesh(self, filepath)

    # The block model handler will save the block model by reading our own data
    # Returns a boolean
    def save_blockmodel(self, filepath):
        return self.blockmodel_handler.save_mesh(self, filepath)
