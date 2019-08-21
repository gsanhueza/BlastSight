#!/usr/bin/env python

from .elements.element import Element
from .elements.elementcollection import ElementCollection
from .elements.blockelement import BlockElement
from .elements.pointelement import PointElement
from .elements.lineelement import LineElement
from .elements.meshelement import MeshElement
from .elements.tubeelement import TubeElement

from .parsers.dxfparser import DXFParser
from .parsers.offparser import OFFParser
from .parsers.h5mparser import H5MParser
from .parsers.h5pparser import H5PParser
from .parsers.csvparser import CSVParser
from .parsers.outparser import OUTParser


class Model:
    def __init__(self):
        self._element_collection = ElementCollection()
        self.parser_dict = {}  # Example: {"dxf": DXFParser}

        self.add_parser('dxf', DXFParser)
        self.add_parser('off', OFFParser)
        self.add_parser('h5m', H5MParser)
        self.add_parser('h5p', H5PParser)
        self.add_parser('csv', CSVParser)
        self.add_parser('out', OUTParser)

    def add_parser(self, extension: str, handler: type) -> None:
        self.parser_dict[extension] = handler

    def get_parser(self, ext: str) -> type:
        return self.parser_dict.get(ext.lower(), None)

    def _element(self, element_type: type, *args, **kwargs):
        element = element_type(*args, **kwargs)
        self.element_collection.add(element)

        return element

    def mesh(self, *args, **kwargs) -> MeshElement:
        return self._element(MeshElement, *args, **kwargs)

    def blocks(self, *args, **kwargs) -> BlockElement:
        return self._element(BlockElement, *args, **kwargs)

    def points(self, *args, **kwargs) -> PointElement:
        return self._element(PointElement, *args, **kwargs)

    def lines(self, *args, **kwargs) -> LineElement:
        return self._element(LineElement, *args, **kwargs)

    def tubes(self, *args, **kwargs) -> TubeElement:
        return self._element(TubeElement, *args, **kwargs)

    def mesh_by_path(self, path: str, *args, **kwargs) -> MeshElement:
        ext = path.split('.')[-1]
        info = self.get_parser(ext).load_file(path)
        vertices = info.vertices
        indices = info.indices
        properties = info.properties

        for k, v in properties.items():
            kwargs[k] = v

        return self.mesh(vertices=vertices, indices=indices, *args, **kwargs)

    def block_model_by_path(self, path: str, *args, **kwargs) -> BlockElement:
        ext = path.split('.')[-1]
        info = self.get_parser(ext).load_file(path)
        data = info.data
        properties = info.properties

        for k, v in properties.items():
            kwargs[k] = v

        return self.blocks(data=data, *args, **kwargs)

    def points_by_path(self, path: str, *args, **kwargs) -> PointElement:
        ext = path.split('.')[-1]
        info = self.get_parser(ext).load_file(path)
        data = info.data
        properties = info.properties

        for k, v in properties.items():
            kwargs[k] = v

        return self.points(data=data, *args, **kwargs)

    def get(self, id_: int) -> Element:
        return self.element_collection[id_]

    def delete(self, id_: int) -> None:
        self.element_collection.delete(id_)

    @property
    def element_collection(self) -> ElementCollection:
        return self._element_collection

    @property
    def mesh_collection(self) -> list:
        return list(filter(lambda x: isinstance(x, MeshElement), self.element_collection.values()))

    @property
    def block_model_collection(self) -> list:
        return list(filter(lambda x: isinstance(x, BlockElement), self.element_collection.values()))
