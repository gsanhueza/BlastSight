#!/usr/bin/env python

from collections import OrderedDict
from Model.Mesh.meshelement import MeshElement
from Model.BlockModel.blockmodelelement import BlockModelElement


# Main class
class Model:
    def __init__(self):
        self.mesh_collection = OrderedDict()
        self.mesh_last_identifier = 0
        self.block_model_collection = []

    def add_mesh(self, file_path: str) -> int:
        mesh = MeshElement()
        mesh.load(file_path)
        self.mesh_collection[self.mesh_last_identifier] = mesh

        self.mesh_last_identifier += 1
        return self.mesh_last_identifier - 1

    def update_mesh(self, id_: int, file_path: str):
        mesh = MeshElement()
        mesh.load(file_path)
        self.mesh_collection[id_] = mesh

    def add_block_model(self, file_path: str) -> None:
        block_model = BlockModelElement()
        block_model.load(file_path)

        self.block_model_collection.append(block_model)

    def delete_mesh(self, id_: int) -> bool:
        self.mesh_collection[id_] = None
        return True

    def get_mesh(self, id_: int) -> MeshElement:
        return self.mesh_collection[id_]

    def get_mesh_collection(self):
        return self.mesh_collection.values()

    def get_block_model(self) -> BlockModelElement:
        return self.block_model_collection[0]

    def get_block_model_collection(self):
        return self.block_model_collection
