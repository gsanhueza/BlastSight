#!/usr/bin/env python

from qtpy.QtCore import QFileInfo

from .Elements.element import Element
from .Elements.elementcollection import ElementCollection
from .Elements.blockmodelelement import BlockModelElement
from .Elements.pointelement import PointElement
from .Elements.lineelement import LineElement
from .Elements.meshelement import MeshElement
from .Elements.tubeelement import TubeElement

from .Parsers.dxfparser import DXFParser
from .Parsers.offparser import OFFParser
from .Parsers.csvparser import CSVParser


class Model:
    def __init__(self):
        self._element_collection = ElementCollection()
        self.parser_dict = {}  # Example: {"dxf": (DXFParser, MeshElement)}

        self.add_parser('dxf', DXFParser, MeshElement)
        self.add_parser('off', OFFParser, MeshElement)
        self.add_parser('csv', CSVParser, BlockModelElement)

    def add_parser(self, extension: str, handler, element_type) -> None:
        self.parser_dict[extension] = (handler, element_type)

    def get_parser(self, ext: str, element_type=None):
        assert self.parser_dict[ext][1] == element_type
        return self.parser_dict[ext][0]

    def _element(self, element_type: type, *args, **kwargs):
        element = element_type(*args, **kwargs)
        self.element_collection.add(element)

        return element

    def mesh(self, *args, **kwargs) -> MeshElement:
        return self._element(MeshElement, *args, **kwargs)

    def block_model(self, *args, **kwargs) -> BlockModelElement:
        return self._element(BlockModelElement, *args, **kwargs)

    def points(self, *args, **kwargs) -> PointElement:
        return self._element(PointElement, *args, **kwargs)

    def lines(self, *args, **kwargs) -> LineElement:
        return self._element(LineElement, *args, **kwargs)

    def tubes(self, *args, **kwargs) -> TubeElement:
        return self._element(TubeElement, *args, **kwargs)

    def mesh_by_path(self, path: str, *args, **kwargs) -> MeshElement:
        name = QFileInfo(path).baseName()
        ext = QFileInfo(path).suffix()
        vertices, indices = self.get_parser(ext, MeshElement).load_file(path)

        return self.mesh(vertices=vertices, indices=indices, name=name, ext=ext, *args, **kwargs)

    def block_model_by_path(self, path: str) -> BlockModelElement:
        name = QFileInfo(path).baseName()
        ext = QFileInfo(path).suffix()
        data = self.get_parser(ext, BlockModelElement).load_file(path)

        return self.block_model(data=data, name=name, ext=ext)

    def get(self, id_: int) -> Element:
        return self.element_collection[id_]

    def delete(self, id_: int) -> None:
        self.element_collection.__delitem__(id_)

    @property
    def element_collection(self) -> ElementCollection:
        return self._element_collection

    @property
    def mesh_collection(self) -> list:
        return list(filter(lambda x: isinstance(x, MeshElement), self.element_collection.values()))

    @property
    def block_model_collection(self) -> list:
        return list(filter(lambda x: isinstance(x, BlockModelElement), self.element_collection.values()))
