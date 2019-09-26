#!/usr/bin/env python

from .elements.element import Element
from .elements.elementcollection import ElementCollection
from .elements.blockelement import BlockElement
from .elements.pointelement import PointElement
from .elements.lineelement import LineElement
from .elements.meshelement import MeshElement
from .elements.tubeelement import TubeElement

from .parsers.parser import Parser
from .parsers.dxfparser import DXFParser
from .parsers.offparser import OFFParser
from .parsers.h5mparser import H5MParser
from .parsers.h5pparser import H5PParser
from .parsers.csvparser import CSVParser
from .parsers.gslibparser import GSLibParser


class Model:
    def __init__(self):
        self._element_collection = ElementCollection()
        self.parser_dict = {}  # Example: {"dxf": DXFParser}

        self.add_parser('dxf', DXFParser)
        self.add_parser('off', OFFParser)
        self.add_parser('h5m', H5MParser)
        self.add_parser('h5p', H5PParser)
        self.add_parser('csv', CSVParser)
        self.add_parser('out', GSLibParser)

    def add_parser(self, extension: str, handler: type) -> None:
        self.parser_dict[extension] = handler

    def get_parser(self, ext: str) -> Parser:
        return self.parser_dict.get(ext.lower(), None)

    """
    Element loading
    """
    def _element(self, element_type: type, *args, **kwargs):
        element = element_type(*args, **kwargs)
        self.element_collection.add(element)

        return element

    def _element_by_path(self, path: str, element_type: type, *args, **kwargs):
        ext = path.split('.')[-1]
        info = self.get_parser(ext).load_file(path)
        data = info.data
        properties = info.properties

        kwargs['data'] = data
        for k, v in properties.items():
            kwargs[k] = v

        return self._element(element_type, *args, **kwargs)

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
        return self._element_by_path(path, MeshElement, *args, **kwargs)

    def blocks_by_path(self, path: str, *args, **kwargs) -> BlockElement:
        return self._element_by_path(path, BlockElement, *args, **kwargs)

    def points_by_path(self, path: str, *args, **kwargs) -> PointElement:
        return self._element_by_path(path, PointElement, *args, **kwargs)

    """
    Element exporting
    """
    def export(self, path: str, _id: int) -> None:
        element = self.get(_id)
        ext = path.split('.')[-1]

        data = element.data
        properties = {}
        for k in element.exportable_properties:
            properties[k] = element.get_property(k)

        self.get_parser(ext).save_file(path=path, data=data, properties=properties)

    def export_mesh(self, path: str, _id: int) -> None:
        self.export(path, _id)

    def export_blocks(self, path: str, _id: int) -> None:
        self.export(path, _id)

    def export_points(self, path: str, _id: int) -> None:
        self.export(path, _id)

    """
    Element handling
    """
    def get(self, _id: int) -> Element:
        return self.element_collection[_id]

    def delete(self, _id: int) -> None:
        self.element_collection.delete(_id)

    @property
    def last_id(self) -> int:
        return self.element_collection.last_id

    @property
    def element_collection(self) -> ElementCollection:
        return self._element_collection
