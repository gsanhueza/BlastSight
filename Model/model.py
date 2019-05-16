#!/usr/bin/env python

import traceback
from PyQt5.QtCore import QFileInfo

from collections import OrderedDict
from Model.element import Element
from Model.Mesh.meshelement import MeshElement
from Model.BlockModel.blockmodelelement import BlockModelElement

from Model.Mesh.dxfparser import DXFParser
from Model.Mesh.offparser import OFFParser
from Model.BlockModel.csvparser import CSVParser


class Model:
    def __init__(self):
        self.element_collection = OrderedDict()
        self.parser_dict = {}  # Example: {"dxf": DXFParser, "off": OFFParser}
        self.last_id = 0

        self.add_parser('dxf', DXFParser)
        self.add_parser('off', OFFParser)
        self.add_parser('csv', CSVParser)

    def add_parser(self, extension: str, handler) -> None:
        self.parser_dict[extension] = handler

    def get_parser(self, ext: str):
        return self.parser_dict[ext]

    def add_mesh(self, file_path: str) -> int:
        try:
            ext = QFileInfo(file_path).suffix()
            vertices, indices = self.get_parser(ext).load_file(file_path)
            # [[x1, y1, z1], [x2, y2, z2]] -> [[x1, x2], [y1, y2], [z1, z2])

            self.element_collection[self.last_id] = MeshElement(vertices=vertices, indices=indices)
            self.last_id += 1

            return self.last_id - 1
        except Exception:
            traceback.print_exc()
            return -1

    def add_block_model(self, file_path: str) -> int:
        try:
            ext = QFileInfo(file_path).suffix()
            data = self.get_parser(ext).load_file(file_path)

            self.element_collection[self.last_id] = BlockModelElement(data=data)
            self.last_id += 1

            return self.last_id - 1
        except Exception:
            traceback.print_exc()
            return -1

    # Generalization of delete
    def delete_element(self, id_: int) -> bool:
        self.element_collection.__delitem__(id_)
        return True

    def delete_mesh(self, id_: int) -> bool:
        return self.delete_element(id_)

    def delete_block_model(self, id_: int) -> bool:
        return self.delete_element(id_)

    # Generalization of get
    def get_element(self, id_: int) -> Element:
        return self.element_collection[id_]

    def get_mesh(self, id_: int) -> Element:
        return self.get_element(id_)

    def get_block_model(self, id_: int) -> Element:
        return self.get_element(id_)

    # Generalization of get collection
    def get_element_collection(self) -> list:
        return list(self.element_collection.items())

    def get_mesh_collection(self) -> list:
        return list(filter(lambda x: isinstance(x[1], MeshElement), self.get_element_collection()))

    def get_block_model_collection(self) -> list:
        return list(filter(lambda x: isinstance(x[1], BlockModelElement), self.get_element_collection()))
