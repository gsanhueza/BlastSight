#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np
from . import utils

from qtpy.QtCore import QDirIterator
from qtpy.QtCore import QFileInfo
from qtpy.QtCore import QMutex
from qtpy.QtCore import QMutexLocker

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
        self._parser_dict = {}  # Example: {"dxf": DXFParser}
        self._mutex = QMutex()

        self.element_collection = ElementCollection()

        self.add_parser('dxf', DXFParser)
        self.add_parser('off', OFFParser)
        self.add_parser('h5m', H5MParser)
        self.add_parser('h5p', H5PParser)
        self.add_parser('csv', CSVParser)
        self.add_parser('out', GSLibParser)

    @property
    def last_id(self) -> int:
        return self.element_collection.last_id

    """
    Utilities
    """
    def add_parser(self, extension: str, handler: type) -> None:
        self._parser_dict[extension] = handler

    def get_parser(self, ext: str) -> Parser:
        return self._parser_dict.get(ext.lower(), None)

    @staticmethod
    def get_paths_from_directory(path: str) -> list:
        it = QDirIterator(path, QDirIterator.Subdirectories)
        path_list = []

        while it.hasNext():
            next_path = it.next()
            if QFileInfo(next_path).isFile():
                path_list.append(next_path)

        return sorted(path_list)

    """
    Element loading
    """
    def _load_element(self, element_type: type, *args, **kwargs):
        element = element_type(*args, **kwargs)

        # In a multi-threaded application, we can't risk assigning
        # the same ID to different elements, so we use a mutex here.
        with QMutexLocker(self._mutex):
            self.element_collection.add(element)

        return element

    def _load_element_by_path(self, path: str, element_type: type, *args, **kwargs):
        ext = path.split('.')[-1]
        info = self.get_parser(ext).load_file(path, *args, **kwargs)
        data = info.data
        properties = info.properties

        kwargs['data'] = data
        for k, v in properties.items():
            kwargs[k] = v

        return self._load_element(element_type, *args, **kwargs)

    def mesh(self, *args, **kwargs) -> MeshElement:
        return self._load_element(MeshElement, *args, **kwargs)

    def blocks(self, *args, **kwargs) -> BlockElement:
        return self._load_element(BlockElement, *args, **kwargs)

    def points(self, *args, **kwargs) -> PointElement:
        return self._load_element(PointElement, *args, **kwargs)

    def lines(self, *args, **kwargs) -> LineElement:
        return self._load_element(LineElement, *args, **kwargs)

    def tubes(self, *args, **kwargs) -> TubeElement:
        return self._load_element(TubeElement, *args, **kwargs)

    def mesh_by_path(self, path: str, *args, **kwargs) -> MeshElement:
        return self._load_element_by_path(path, MeshElement, *args, **kwargs)

    def blocks_by_path(self, path: str, *args, **kwargs) -> BlockElement:
        return self._load_element_by_path(path, BlockElement, *args, **kwargs)

    def points_by_path(self, path: str, *args, **kwargs) -> PointElement:
        return self._load_element_by_path(path, PointElement, *args, **kwargs)

    def lines_by_path(self, path: str, *args, **kwargs) -> LineElement:
        return self._load_element_by_path(path, LineElement, *args, **kwargs)

    def tubes_by_path(self, path: str, *args, **kwargs) -> TubeElement:
        return self._load_element_by_path(path, TubeElement, *args, **kwargs)

    """
    Element handling
    """
    def get(self, _id: int) -> Element:
        return self.element_collection.get(_id, None)

    def delete(self, _id: int) -> None:
        self.element_collection.delete(_id)

    """
    Element exporting
    """
    def export(self, path: str, _id: int) -> None:
        element = self.get(_id)
        ext = path.split('.')[-1]

        data = element.data
        properties = {}
        for k in element.exportable_properties:
            properties[k] = getattr(element, k)

        self.get_parser(ext).save_file(path=path, data=data, properties=properties)

    def export_mesh(self, path: str, _id: int) -> None:
        self.export(path, _id)

    def export_blocks(self, path: str, _id: int) -> None:
        self.export(path, _id)

    def export_points(self, path: str, _id: int) -> None:
        self.export(path, _id)

    def export_lines(self, path: str, _id: int) -> None:
        self.export(path, _id)

    def export_tubes(self, path: str, _id: int) -> None:
        self.export(path, _id)

    """
    Adapter for viewer's utilities (slice/distance)
    """
    @staticmethod
    def slice_meshes(origin: np.ndarray, plane_normal: np.ndarray, meshes: list) -> dict:
        """
        Returns a dict with the following structure:

        {
            'plane_origin': list(float),
            'plane_normal': list(float)',
            'slices': [{
                'origin_id': int,
                'vertices': list(list(float))
            }]
        }
        """
        return {
            'plane_origin': origin,
            'plane_normal': plane_normal,
            'slices': [
                {
                    'origin_id': mesh.id,
                    'vertices': utils.slice_mesh(mesh, origin, plane_normal)
                } for mesh in meshes]
        }

    @staticmethod
    def slice_blocks(origin: np.ndarray, plane_normal: np.ndarray, block_list: list) -> dict:
        """
        Returns a dict with the following structure:

        {
            'plane_origin': list(float),
            'plane_normal': list(float)',
            'slices': [{
                'origin_id': int,
                'indices': list(int)
            }]
        }
        """
        return {
            'plane_origin': origin,
            'plane_normal': plane_normal,
            'slices': [
                {
                    'origin_id': block.id,
                    'indices': utils.slice_blocks(block, block.block_size, origin, plane_normal)
                } for block in block_list]
        }

    @staticmethod
    def measure_from_rays(origin_list: list, ray_list: list, meshes: list) -> dict:
        """
        Returns a dict with the following structure:

        {
            'point_a': list(float) or None,
            'point_b': list(float) or None',
            'distance': float or None
        }
        """
        points_A = []
        points_B = []

        closest_A = None
        closest_B = None

        # Detect intersections
        for mesh in meshes:
            int_A = utils.mesh_intersection(origin_list[0], ray_list[0], mesh)
            int_B = utils.mesh_intersection(origin_list[1], ray_list[1], mesh)

            # Discard non-intersections
            if int_A.size > 0:
                points_A.append(utils.closest_point_to(origin_list[0], int_A))

            if int_B.size > 0:
                points_B.append(utils.closest_point_to(origin_list[1], int_B))

        # Get closest points for each origin
        if len(points_A) > 0:
            points_A = np.vstack(points_A)
            closest_A = utils.closest_point_to(origin_list[0], points_A)

        if len(points_B) > 0:
            points_B = np.vstack(points_B)
            closest_B = utils.closest_point_to(origin_list[1], points_B)

        # Calculate distance if possible
        try:
            distance = np.linalg.norm(closest_B - closest_A)
        except TypeError:
            distance = None

        return {
            'point_a': closest_A,
            'point_b': closest_B,
            'distance': distance,
        }
