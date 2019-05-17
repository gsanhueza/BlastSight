#!/usr/bin/env python

import traceback
from collections import OrderedDict

from PyQt5.QtCore import QFileInfo

from Model.Elements.element import Element
from Model.Elements.meshelement import MeshElement
from Model.Elements.blockmodelelement import BlockModelElement

from Model.Parsers.dxfparser import DXFParser
from Model.Parsers.offparser import OFFParser
from Model.Parsers.csvparser import CSVParser


class Model:
    def __init__(self):
        self.element_collection = OrderedDict()
        self.parser_dict = {}  # Example: {"dxf": (DXFParser, MeshElement)}
        self.last_id = 0

        self.add_parser('dxf', DXFParser, MeshElement)
        self.add_parser('off', OFFParser, MeshElement)
        self.add_parser('csv', CSVParser, BlockModelElement)

    def add_parser(self, extension: str, handler, element_type) -> None:
        self.parser_dict[extension] = (handler, element_type)

    def get_parser(self, ext: str, element_type=None):
        if element_type is not None:
            assert self.parser_dict[ext][1] == element_type
        return self.parser_dict[ext][0]

    def add_mesh(self, file_path: str) -> int:
        try:
            name = QFileInfo(file_path).baseName()
            ext = QFileInfo(file_path).suffix()
            vertices, indices = self.get_parser(ext, MeshElement).load_file(file_path)
            # [[x1, y1, z1], [x2, y2, z2]] -> [[x1, x2], [y1, y2], [z1, z2])

            self.element_collection[self.last_id] = MeshElement(vertices=vertices,
                                                                indices=indices,
                                                                name=name,
                                                                ext=ext)
            self.last_id += 1

            return self.last_id - 1
        except Exception:
            traceback.print_exc()
            return -1

    def add_block_model(self, file_path: str) -> int:
        try:
            name = QFileInfo(file_path).baseName()
            ext = QFileInfo(file_path).suffix()
            data = self.get_parser(ext, BlockModelElement).load_file(file_path)

            self.element_collection[self.last_id] = BlockModelElement(data=data,
                                                                      name=name,
                                                                      ext=ext)
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
