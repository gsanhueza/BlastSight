#!/usr/bin/env python

from Model.Mesh.meshelement import MeshElement
from Model.BlockModel.blockmodelelement import BlockModelElement


# Main class
class Model:
    def __init__(self):
        self.mesh_collection = {}
        self.mesh_last_identifier = 0
        self.block_model = None

    def add_mesh(self, file_path: str) -> int:
        self.mesh_last_identifier += 1

        mesh = MeshElement()
        mesh.load(file_path)
        self.mesh_collection[self.mesh_last_identifier] = mesh

        return self.mesh_last_identifier

    def add_block_model(self, file_path: str) -> None:
        self.block_model = BlockModelElement()
        self.block_model.load(file_path)

    def delete_mesh(self, _id: int) -> bool:
        self.mesh_collection[_id] = None
        return True

    def get_mesh(self, _id: int) -> MeshElement:
        return self.mesh_collection[_id]

    def get_meshes(self):
        return self.mesh_collection.values()

    def get_block_model(self) -> BlockModelElement:
        return self.block_model
