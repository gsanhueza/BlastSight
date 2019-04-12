#!/usr/bin/env python

from Model.Mesh.meshelement import MeshElement
from Model.BlockModel.blockmodelelement import BlockModelElement


# Main class
class Model:
    def __init__(self):
        self.mesh = MeshElement()
        self.block_model = BlockModelElement()

    def get_mesh(self):
        return self.mesh

    def get_block_model(self):
        return self.block_model
