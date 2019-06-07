#!/usr/bin/env python

from collections import OrderedDict

from qtpy.QtCore import QFileInfo

from Model.Elements.element import Element
from Model.Elements.blockmodelelement import BlockModelElement
from Model.Elements.lineelement import LineElement
from Model.Elements.meshelement import MeshElement
from Model.Elements.tubeelement import TubeElement

from Model.Parsers.dxfparser import DXFParser
from Model.Parsers.offparser import OFFParser
from Model.Parsers.csvparser import CSVParser


class Model:
    def __init__(self):
        self._element_collection = OrderedDict()
        self.parser_dict = {}  # Example: {"dxf": (DXFParser, MeshElement)}
        self.last_id = 0

        self.add_parser('dxf', DXFParser, MeshElement)
        self.add_parser('off', OFFParser, MeshElement)
        self.add_parser('csv', CSVParser, BlockModelElement)

    def add_parser(self, extension: str, handler, element_type) -> None:
        self.parser_dict[extension] = (handler, element_type)

    def get_parser(self, ext: str, element_type=None):
        assert self.parser_dict[ext][1] == element_type
        return self.parser_dict[ext][0]

    def mesh(self, *args, **kwargs) -> MeshElement:
        element = MeshElement(*args, **kwargs)
        element.id = self.last_id

        self._element_collection[self.last_id] = element
        self.last_id += 1

        return element

    def mesh_by_path(self, path: str, *args, **kwargs) -> MeshElement:
        name = QFileInfo(path).baseName()
        ext = QFileInfo(path).suffix()
        vertices, indices = self.get_parser(ext, MeshElement).load_file(path)

        return self.mesh(vertices=vertices, indices=indices, name=name, ext=ext, *args, **kwargs)

    def block_model(self, *args, **kwargs) -> BlockModelElement:
        element = BlockModelElement(*args, **kwargs)
        element.id = self.last_id

        self._element_collection[self.last_id] = element
        self.last_id += 1

        return element

    def block_model_by_path(self, path: str) -> BlockModelElement:
        name = QFileInfo(path).baseName()
        ext = QFileInfo(path).suffix()
        data = self.get_parser(ext, BlockModelElement).load_file(path)

        return self.block_model(data=data, name=name, ext=ext)

    def lines(self, *args, **kwargs) -> LineElement:
        element = LineElement(*args, **kwargs)
        element.id = self.last_id

        self._element_collection[self.last_id] = element
        self.last_id += 1

        return element

    def tubes(self, *args, **kwargs) -> LineElement:
        element = TubeElement(*args, **kwargs)
        element.id = self.last_id

        self._element_collection[self.last_id] = element
        self.last_id += 1

        return element

    def get(self, id_: int) -> Element:
        return self._element_collection[id_]

    def delete(self, id_: int) -> None:
        self._element_collection.__delitem__(id_)

    @property
    def element_collection(self) -> list:
        return list(self._element_collection.items())

    @property
    def mesh_collection(self) -> list:
        return list(filter(lambda x: isinstance(x, MeshElement), self._element_collection.values()))

    @property
    def block_model_collection(self) -> list:
        return list(filter(lambda x: isinstance(x, BlockModelElement), self._element_collection.values()))
