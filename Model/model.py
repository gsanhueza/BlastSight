#!/usr/bin/env python

from collections import OrderedDict
from Model.modelelement import ModelElement
from Model.Mesh.meshelement import MeshElement
from Model.BlockModel.blockmodelelement import BlockModelElement


# Main class
class Model:
    def __init__(self):
        self.element_collection = OrderedDict()
        self.last_id = 0

    # Generalization of add
    def add_element(self, file_path: str, element: ModelElement) -> int:
        if element.load(file_path):
            self.element_collection[self.last_id] = element
            self.last_id += 1

            return self.last_id - 1
        return -1

    def add_mesh(self, file_path: str) -> int:
        mesh = MeshElement()
        return self.add_element(file_path, mesh)

    def add_block_model(self, file_path: str) -> int:
        block_model = BlockModelElement()
        return self.add_element(file_path, block_model)

    # Generalization of update
    def update_element(self, id_: int, file_path: str, element: ModelElement) -> None:
        element.load(file_path)
        self.element_collection[id_] = element

    def update_mesh(self, id_: int, file_path: str) -> None:
        mesh = MeshElement()
        self.update_element(id_, file_path, mesh)

    def update_block_model(self, id_: int, file_path: str) -> None:
        block_model = BlockModelElement()
        self.update_element(id_, file_path, block_model)

    # Generalization of delete
    def delete_element(self, id_: int) -> bool:
        self.element_collection.__delitem__(id_)
        return True

    def delete_mesh(self, id_: int) -> bool:
        return self.delete_element(id_)

    def delete_block_model(self, id_: int) -> bool:
        return self.delete_element(id_)

    # Generalization of get
    def get_element(self, id_: int) -> ModelElement:
        return self.element_collection[id_]

    def get_mesh(self, id_: int) -> ModelElement:
        return self.get_element(id_)

    def get_block_model(self, id_: int) -> ModelElement:
        return self.get_element(id_)

    # Generalization of get collection
    def get_element_collection(self) -> list:
        return list(self.element_collection.items())

    def get_mesh_collection(self) -> list:
        return list(filter(lambda x: isinstance(x[1], MeshElement), self.get_element_collection()))

    def get_block_model_collection(self) -> list:
        return list(filter(lambda x: isinstance(x[1], BlockModelElement), self.get_element_collection()))
