#!/usr/bin/env python

from collections import OrderedDict
from Model.Mesh.meshelement import MeshElement
from Model.BlockModel.blockmodelelement import BlockModelElement


# Main class
class Model:
    def __init__(self):
        self.mesh_collection = OrderedDict()
        self.block_model_collection = OrderedDict()
        self.last_id = 0

    def add_mesh(self, file_path: str) -> int:
        mesh = MeshElement()
        mesh.load(file_path)
        self.mesh_collection[self.last_id] = mesh

        self.last_id += 1
        return self.last_id - 1

    def add_block_model(self, file_path: str) -> int:
        block_model = BlockModelElement()
        block_model.load(file_path)

        self.block_model_collection[self.last_id] = block_model

        self.last_id += 1
        return self.last_id - 1

    def update_mesh(self, id_: int, file_path: str) -> None:
        mesh = MeshElement()
        mesh.load(file_path)
        self.mesh_collection[id_] = mesh

    def delete_block_model(self, id_: int) -> bool:
        self.block_model_collection[id_] = None
        return True

    def update_block_model(self, id_: int, file_path: str) -> None:
        block_model = BlockModelElement()
        block_model.load(file_path)
        self.block_model_collection[id_] = block_model

    def delete_mesh(self, id_: int) -> bool:
        self.mesh_collection[id_] = None
        return True

    def get_mesh(self, id_: int) -> MeshElement:
        return self.mesh_collection[id_]

    def get_mesh_collection(self):
        return self.mesh_collection.items()

    def get_block_model(self, id_: int) -> BlockModelElement:
        return self.block_model_collection[id_]

    def get_block_model_collection(self):
        return self.block_model_collection.items()
